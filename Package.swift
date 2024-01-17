// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "DFSOptimizer",
    dependencies: [
        .package(url: "https://github.com/ealmada90/DFSOptimizer.git", from: "0.1"),
    ],
    targets: [
        .executableTarget(
            name: "DFSOptimizer",
            dependencies: ["DFSOptimizer"]),
    ]
)