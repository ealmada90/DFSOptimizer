//
//  File.swift
//  DFSOptimizerPackage
//
//  Created by Elioth Almada on 1/16/24.
//

import PackageDescription

let package = Package(
        name: "DFSOptimizer",
        products: [
            .library(name: "DFSOptimizer", targets: ["DFSOptimizer"])
        ],
        dependencies: [],
        targets: [
            .target(name: "DFSOptimizer",
                    path: "Sources")
        ]
)
