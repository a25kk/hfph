vcl 4.0;

import std;

# Configure balancer server as back end
backend balancer {
    .host = "${hosts:varnish-backend}";
    .port = "${ports:varnish-backend}";
    .connect_timeout = 0.4s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout = 60s;
}

# Only allow PURGE from localhost
acl purge {
    "${hosts:allow-purge}";
}

sub vcl_hit {
  if (obj.ttl >= 0s) {
    # normal hit
    return (deliver);
  }
  # We have no fresh fish. Lets look at the stale ones.
  if (std.healthy(req.backend_hint)) {
    # Backend is healthy. Limit age to 10s.
    if (obj.ttl + 10s > 0s) {
      set req.http.grace = "normal(limited)";
      return (deliver);
    } else {
      # No candidate for grace. Fetch a fresh object.
      return(fetch);
   }
  } else {
    # backend is sick - use full grace
    if (obj.ttl + obj.grace > 0s) {
      set req.http.grace = "full";
      return (deliver);
    } else {
     # no graced object.
    return (fetch);
   }
  }
}

sub vcl_recv {
    set req.backend_hint = balancer;
    set req.http.grace = "none";

    if (req.method == "PURGE") {
        if (!client.ip ~ purge) {
            return(synth(405, "Not allowed."));
        }
        ban("req.http.host == " + req.http.host +
                      "&& req.url == " + req.url);
        return(synth(200, "Ban added"));
    }
    if (req.method != "GET" && req.method != "HEAD") {
        # We only deal with GET and HEAD by default
        return(pass);
    }
    if (req.http.host ~ "^(.*\.)?coraggio\.de$" || req.http.host ~ "^(.*\.)?kreativkombinat.de$") {
        # We do not cache sites in development
        return(pass);
    }
    call normalize_accept_encoding;
    call annotate_request;
    return(hash);
}

sub vcl_backend_response {
    set beresp.ttl = 10s;
    set beresp.grace = 1h;
    if (!beresp.ttl > 0s) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - not cacheable)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }
    if (beresp.http.Set-Cookie) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets cookie)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }
    if (!beresp.http.Cache-Control ~ "s-maxage=[1-9]" && beresp.http.Cache-Control ~ "(private|no-cache|no-store)") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets private/no-cache/no-store token)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }
    if (!bereq.http.X-Anonymous && !beresp.http.Cache-Control ~ "public") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - authorized and no public cache control)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }
    if (bereq.http.X-Anonymous && !beresp.http.Cache-Control) {
        set beresp.ttl = 10s;
        set beresp.http.X-Varnish-Action = "FETCH (override - backend not setting cache control)";
    } else {
        set beresp.http.X-Varnish-Action = "FETCH (deliver)";
    }
    call rewrite_s_maxage;
    return(deliver);
}

sub vcl_deliver {
    call rewrite_age;
    set resp.http.grace = req.http.grace;
}

##########################
#  Helper Subroutines
##########################

# Optimize the Accept-Encoding variant caching
sub normalize_accept_encoding {
    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(jpe?g|png|gif|swf|pdf|gz|tgz|bz2|tbz|zip)$" || req.url ~ "/image_[^/]*$") {
            unset req.http.Accept-Encoding;
        } elsif (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } else {
            unset req.http.Accept-Encoding;
        }
    }
}

# Keep auth/anon variants apart if "Vary: X-Anonymous" is in the response
sub annotate_request {
    if (!(req.http.Authorization || req.http.cookie ~ "(^|.*; )__ac=")) {
        set req.http.X-Anonymous = "True";
    }
}

# The varnish response should always declare itself to be fresh
sub rewrite_age {
    if (resp.http.Age) {
        set resp.http.X-Varnish-Age = resp.http.Age;
        set resp.http.Age = "0";
    }
}

# Rewrite s-maxage to exclude from intermediary proxies
# (to cache *everywhere*, just use 'max-age' token in the response to avoid this override)
sub rewrite_s_maxage {
    if (beresp.http.Cache-Control ~ "s-maxage") {
        set beresp.http.Cache-Control = regsub(beresp.http.Cache-Control, "s-maxage=[0-9]+", "s-maxage=0");
    }
}
