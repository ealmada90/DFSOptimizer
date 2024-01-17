//  swift-tools-version:5.9

//  Package.swift
//  LineStarForYahoo
//
//  Created by Elioth Almada on 1/17/24.
//  Copyright © 2024 fantasysportsco. All rights reserved.
//


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