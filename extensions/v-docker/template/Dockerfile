FROM ghcr.io/vlang/vlang:latest AS build
WORKDIR /app
COPY . .
RUN v -prod -o /app/bin/app .

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=build /app/bin/app /app/app
EXPOSE 8080
CMD ["/app/app"]
