FROM alpine:3.20
RUN apk add --no-cache bash
COPY . /app
RUN chmod +x /app/collect.sh
CMD ["/app/collect.sh"]
