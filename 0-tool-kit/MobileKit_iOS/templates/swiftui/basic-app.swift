//
//  BasicApp.swift
//  MobileKit iOS Template
//
//  Created by MobileKit on $(date)
//

import SwiftUI
import Combine

@main
struct MyiOSAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                // Header
                VStack(spacing: 8) {
                    Image(systemName: "iphone")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)

                    Text("Welcome to MobileKit iOS")
                        .font(.title)
                        .fontWeight(.bold)

                    Text("AI-Powered iOS Development")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .padding()

                // Features List
                LazyVStack(spacing: 16) {
                    ForEach(viewModel.features) { feature in
                        FeatureRow(feature: feature)
                    }
                }
                .padding(.horizontal)

                Spacer()

                // Get Started Button
                Button(action: {
                    viewModel.getStarted()
                }) {
                    HStack {
                        Image(systemName: "rocket.fill")
                        Text("Get Started")
                    }
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(12)
                }
                .padding(.horizontal)
            }
            .navigationTitle("MobileKit iOS")
            .navigationBarTitleDisplayMode(.inline)
        }
        .task {
            await viewModel.loadFeatures()
        }
    }
}

struct FeatureRow: View {
    let feature: Feature

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: feature.icon)
                .font(.title2)
                .foregroundColor(feature.color)
                .frame(width: 30)

            VStack(alignment: .leading, spacing: 4) {
                Text(feature.title)
                    .font(.headline)

                Text(feature.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}

// MARK: - ViewModel
@MainActor
class ContentViewModel: ObservableObject {
    @Published var features: [Feature] = []

    func loadFeatures() async {
        features = [
            Feature(
                icon: "brain.head.profile",
                title: "AI Agents",
                description: "12 specialized AI agents for iOS development",
                color: .purple
            ),
            Feature(
                icon: "swift",
                title: "SwiftUI Components",
                description: "Production-ready SwiftUI components",
                color: .orange
            ),
            Feature(
                icon: "checkmark.shield",
                title: "Testing Suite",
                description: "Comprehensive XCTest and UI testing",
                color: .green
            ),
            Feature(
                icon: "app.badge",
                title: "App Store Ready",
                description: "Automated submission and optimization",
                color: .blue
            )
        ]
    }

    func getStarted() {
        // Navigate to main app flow
        print("🚀 Starting iOS development with MobileKit!")
    }
}

// MARK: - Models
struct Feature: Identifiable {
    let id = UUID()
    let icon: String
    let title: String
    let description: String
    let color: Color
}

#Preview {
    ContentView()
}
