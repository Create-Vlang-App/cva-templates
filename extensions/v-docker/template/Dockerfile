FROM ghcr.io/vlang/vlang:0.5.2 AS build
WORKDIR /app
COPY . .
RUN v -prod -o /app/bin/app .

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=build /app/bin/app /app/app
EXPOSE 8080
CMD ["/app/app"]
