.PHONY: all build run test bench clean examples help

# Default target
all: build

# Build the project
build:
	go build -o bin/kruskal main.go examples.go

# Run the main program
run:
	go run main.go examples.go

# Run all tests
test:
	go test -v

# Run benchmarks
bench:
	go test -bench=. -benchmem

# Run tests with coverage
coverage:
	go test -cover -coverprofile=coverage.out
	go tool cover -html=coverage.out -o coverage.html

# Run only the examples
examples:
	go run examples.go main.go

# Format code
fmt:
	go fmt ./...

# Vet code for issues
vet:
	go vet ./...

# Run linter (requires golangci-lint)
lint:
	golangci-lint run

# Clean build artifacts
clean:
	rm -rf bin/
	rm -f coverage.out coverage.html

# Install dependencies
deps:
	go mod tidy
	go mod download

# Create release build
release:
	mkdir -p bin/
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o bin/kruskal-linux-amd64 main.go examples.go
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -ldflags="-s -w" -o bin/kruskal-darwin-amd64 main.go examples.go
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o bin/kruskal-windows-amd64.exe main.go examples.go

# Display help
help:
	@echo "Available targets:"
	@echo "  all       - Build the project (default)"
	@echo "  build     - Build the executable"
	@echo "  run       - Run the main program"
	@echo "  test      - Run all tests"
	@echo "  bench     - Run benchmarks"
	@echo "  coverage  - Generate test coverage report"
	@echo "  examples  - Run only the examples"
	@echo "  fmt       - Format code"
	@echo "  vet       - Vet code for issues"
	@echo "  lint      - Run linter (requires golangci-lint)"
	@echo "  clean     - Clean build artifacts"
	@echo "  deps      - Install/update dependencies"
	@echo "  release   - Create release builds for multiple platforms"
	@echo "  help      - Display this help message"