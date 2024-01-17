//
//  Package.swift
//  LineStarForYahoo
//
//  Created by Elioth Almada on 1/17/24.
//  Copyright © 2024 fantasysportsco. All rights reserved.
//

// swift-tools-version:5.5
import PackageDescription

let package = Package(
        name: "OptimizerApp",
        products: [
            .library(name: "OptimizerApp", targets: ["Optimizer"])
        ],
        dependencies: [],
        targets: [
            .target(name: "Optimizer",
                    path: "Sources")
        ]
)