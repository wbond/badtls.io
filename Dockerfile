# Usage:
#   $ docker build -t badtls.io .
#   $ docker run --name badtlsio --rm -p 9990:9990 -p 9991:9991 -p 10000:10000 -p 10001:10001 -p 10002:10002 -p 10004:10004 -p 10005:10005 -p 11000:11000 -p 11001:11001 -p 11002:11002 -p 11003:11003 -p 11004:11004 -p 11005:11005 -p 11006:11006 -p 11007:11007 -p 11008:11008 -p 11009:11009 -it badtls.io
#
# Add to /etc/hosts:
# ::1 domain-match.badtls.io wildcard-match.badtls.io san-match.badtls.io required-auth.badtls.io optional-auth.badtls.io dh1024.badtls.io expired-1963.badtls.io future.badtls.io domain-mismatch.badtls.io san-mismatch.badtls.io weak-sig.badtls.io bad-key-usage.badtls.io expired.badtls.io wildcard.mismatch.badtls.io rc4.badtls.io rc4-md5.badtls.io

FROM nginx:latest

ADD . /badtls.io
WORKDIR /badtls.io
RUN rm -rf /etc/nginx/ \
    && ln -s /badtls.io/nginx /etc/nginx \
    && ln -s /badtls.io/certs /etc/certs \
    && mkdir -p /badtls.io/tmp/client_body_temp \
                /badtls.io/logs \
    && sed -e 's#root  ../wwwroot#root /badtls.io/nginx/wwwroot#' -i /badtls.io/nginx/conf/badtls.conf

EXPOSE 9990 9991 10000 10001 10002 10004 10005 11000 11001 11002 11003 11004 11005 11006 11007 11008 11009

CMD ["nginx", "-c", "conf/nginx.conf"]
