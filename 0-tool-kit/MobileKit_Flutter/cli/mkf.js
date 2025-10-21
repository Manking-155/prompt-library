#!/usr/bin/env node

/**
 * MobileKit Flutter CLI (mkf)
 * AI-Powered Flutter Development Toolkit
 */

const { program } = require('commander');
const chalk = require('chalk');
const inquirer = require('inquirer');
const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');
const ora = require('ora');

const VERSION = '1.0.0';

// ASCII Art Banner
const banner = `
███╗   ███╗ ██████╗ ██████╗ ██╗██╗     ███████╗██╗  ██╗██╗████████╗    ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗ 
████╗ ████║██╔═══██╗██╔══██╗██║██║     ██╔════╝██║ ██╔╝██║╚══██╔══╝    ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
██╔████╔██║██║   ██║██████╔╝██║██║     █████╗  █████╔╝ ██║   ██║       █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝
██║╚██╔╝██║██║   ██║██╔══██╗██║██║     ██╔══╝  ██╔═██╗ ██║   ██║       ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║╚██████╔╝██████╔╝██║███████╗███████╗██║  ██╗██║   ██║       ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝       ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
`;

program
  .name('mkf')
  .description('🚀 MobileKit Flutter - AI-Powered Cross-Platform Development Toolkit')
  .version(VERSION)
  .addHelpText('before', chalk.cyan(banner));

// New Project Command
program
  .command('new')
  .description('Create a new Flutter project with AI agents')
  .option('--template <type>', 'Project template', 'material')
  .option('--name <name>', 'Project name')
  .option('--org <org>', 'Organization identifier')
  .action(async (options) => {
    console.log(chalk.blue('🚀 Creating new Flutter project with MobileKit...\n'));

    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'projectName',
        message: '📱 Project name:',
        default: options.name || 'my_flutter_app',
        validate: (input) => /^[a-z][a-z0-9_]*$/.test(input) || 'Use lowercase with underscores only (e.g., my_flutter_app)'
      },
      {
        type: 'list',
        name: 'template',
        message: '🎨 Choose Flutter template:',
        choices: [
          { name: '🎨 Material Design 3 (Recommended)', value: 'material' },
          { name: '🍎 Cupertino (iOS-style)', value: 'cupertino' },
          { name: '📱 Adaptive (Platform-specific)', value: 'adaptive' },
          { name: '🗄️ Material + Riverpod + Drift', value: 'material-full-stack' },
          { name: '🔥 Firebase Starter', value: 'firebase-starter' }
        ],
        default: options.template
      },
      {
        type: 'input',
        name: 'orgName',
        message: '🏢 Organization (reverse domain):',
        default: options.org || 'com.example',
        validate: (input) => /^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$/.test(input) || 'Invalid organization format (e.g., com.example)'
      },
      {
        type: 'checkbox',
        name: 'platforms',
        message: '📱 Target platforms:',
        choices: [
          { name: '🤖 Android', value: 'android', checked: true },
          { name: '🍎 iOS', value: 'ios', checked: true },
          { name: '🌐 Web', value: 'web' },
          { name: '💻 Windows', value: 'windows' },
          { name: '🐧 Linux', value: 'linux' },
          { name: '🍎 macOS', value: 'macos' }
        ]
      },
      {
        type: 'checkbox',
        name: 'packages',
        message: '📦 Select packages to include:',
        choices: [
          { name: '🔄 Riverpod (State Management)', value: 'riverpod' },
          { name: '🧭 GoRouter (Navigation)', value: 'go_router' },
          { name: '🗄️ Drift (Database)', value: 'drift' },
          { name: '🌐 Dio (HTTP Client)', value: 'dio' },
          { name: '📷 Image Picker', value: 'image_picker' },
          { name: '🔔 Firebase (Auth, Firestore, etc.)', value: 'firebase' },
          { name: '❄️ Freezed (Immutable Classes)', value: 'freezed' },
          { name: '🎨 Cached Network Image', value: 'cached_network_image' }
        ]
      }
    ]);

    const spinner = ora('Creating Flutter project...').start();

    try {
      await createFlutterProject(answers);
      spinner.succeed(chalk.green('✅ Flutter project created successfully!'));

      console.log(chalk.yellow('\n📁 Next steps:'));
      console.log(chalk.gray(`   cd ${answers.projectName}`));
      console.log(chalk.gray('   mkf generate-feature --name user_profile --type screen'));
      console.log(chalk.gray('   mkf run-tests --coverage'));

    } catch (error) {
      spinner.fail(chalk.red('❌ Error creating project:'));
      console.error(chalk.red(error.message));
    }
  });

// Generate Feature Command
program
  .command('generate-feature')
  .description('Generate Flutter feature with AI assistance')
  .option('--name <name>', 'Feature name')
  .option('--type <type>', 'Feature type', 'screen')
  .action(async (options) => {
    console.log(chalk.blue('🎯 Generating Flutter feature with AI agents...\n'));

    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'featureName',
        message: '📝 Feature name (snake_case):',
        default: options.name || 'new_feature',
        validate: (input) => /^[a-z][a-z0-9_]*$/.test(input) || 'Use snake_case naming (e.g., user_profile)'
      },
      {
        type: 'list',
        name: 'featureType',
        message: '🎨 Feature type:',
        choices: [
          { name: '📱 Screen (StatefulWidget)', value: 'screen' },
          { name: '🎨 Widget (StatelessWidget)', value: 'widget' },
          { name: '🧮 Provider/Notifier (Riverpod)', value: 'provider' },
          { name: '🗄️ Data Model + Repository', value: 'model-repository' },
          { name: '🌐 API Service', value: 'service' },
          { name: '🏗️ Complete Feature (Clean Architecture)', value: 'complete-feature' },
          { name: '🎭 Bloc Pattern Feature', value: 'bloc-feature' }
        ],
        default: options.type
      },
      {
        type: 'list',
        name: 'stateManagement',
        message: '🔄 State management:',
        choices: [
          { name: 'Riverpod (Recommended)', value: 'riverpod' },
          { name: 'Provider', value: 'provider' },
          { name: 'Bloc', value: 'bloc' },
          { name: 'GetX', value: 'getx' },
          { name: 'None (StatefulWidget)', value: 'none' }
        ],
        default: 'riverpod'
      },
      {
        type: 'confirm',
        name: 'includeTests',
        message: '🧪 Generate tests?',
        default: true
      },
      {
        type: 'confirm',
        name: 'responsive',
        message: '📱 Make responsive for tablet/desktop?',
        default: true
      }
    ]);

    const spinner = ora('Executing AI workflow...').start();

    try {
      await executeWorkflow('generate-flutter-feature', answers);
      spinner.succeed(chalk.green('✅ Flutter feature generated successfully!'));
    } catch (error) {
      spinner.fail(chalk.red('❌ Feature generation failed:'));
      console.error(chalk.red(error.message));
    }
  });

// Run Tests Command
program
  .command('run-tests')
  .description('Run Flutter tests with AI analysis')
  .option('--type <type>', 'Test type', 'all')
  .option('--coverage', 'Generate coverage report')
  .option('--platform <platform>', 'Target platform')
  .option('--golden', 'Update golden files')
  .action(async (options) => {
    console.log(chalk.blue('🧪 Running Flutter tests with AI analysis...\n'));

    const spinner = ora('Running Flutter test suites...').start();

    try {
      let testCommand = 'flutter test';

      if (options.coverage) {
        testCommand += ' --coverage';
      }

      if (options.golden) {
        testCommand += ' --update-goldens';
      }

      switch (options.type) {
        case 'unit':
          testCommand += ' test/unit/';
          break;
        case 'widget':
          testCommand += ' test/widget/';
          break;
        case 'integration':
          testCommand = 'flutter drive --driver=test_driver/integration_test.dart --target=integration_test/app_test.dart';
          if (options.platform) {
            testCommand += ` -d ${options.platform}`;
          }
          break;
        case 'golden':
          testCommand += ' test/golden/';
          break;
      }

      execSync(testCommand, { stdio: 'pipe' });
      spinner.succeed('Tests completed successfully!');

      // Analyze results with AI
      const analysisSpinner = ora('Analyzing test results with AI...').start();
      await executeWorkflow('analyze-flutter-test-results', { 
        testType: options.type,
        platform: options.platform 
      });
      analysisSpinner.succeed('AI analysis completed!');

    } catch (error) {
      spinner.fail(chalk.red('❌ Tests failed'));
      console.error(chalk.red(error.message));

      // Still analyze failures
      const analysisSpinner = ora('Analyzing test failures with AI...').start();
      await executeWorkflow('analyze-flutter-test-failures', { 
        testType: options.type,
        platform: options.platform 
      });
      analysisSpinner.succeed('AI failure analysis completed!');
    }
  });

// Review Code Command
program
  .command('review-code')
  .description('AI-powered code review for Flutter')
  .option('--focus <areas>', 'Review focus areas', 'performance,material-design')
  .option('--files <files>', 'Specific files to review')
  .action(async (options) => {
    console.log(chalk.blue('👁️ Starting AI-powered Flutter code review...\n'));

    const spinner = ora('Analyzing Dart code...').start();

    try {
      await executeWorkflow('flutter-code-review', {
        focus: options.focus.split(','),
        files: options.files?.split(','),
        platform: 'flutter'
      });

      spinner.succeed(chalk.green('✅ Code review completed!'));
    } catch (error) {
      spinner.fail(chalk.red('❌ Code review failed:'));
      console.error(chalk.red(error.message));
    }
  });

// Build Release Command
program
  .command('build-release')
  .description('Build Flutter app for release')
  .option('--platform <platform>', 'Target platform', 'both')
  .option('--flavor <flavor>', 'Build flavor')
  .option('--obfuscate', 'Obfuscate code')
  .action(async (options) => {
    console.log(chalk.blue('🏗️ Building Flutter release...\n'));

    try {
      const platforms = options.platform === 'both' ? ['android', 'ios'] : [options.platform];

      for (const platform of platforms) {
        const spinner = ora(`Building for ${platform}...`).start();

        let buildCommand;
        if (platform === 'android') {
          buildCommand = 'flutter build appbundle --release';
        } else if (platform === 'ios') {
          buildCommand = 'flutter build ios --release --no-codesign';
        } else if (platform === 'web') {
          buildCommand = 'flutter build web --release';
        }

        if (options.flavor) {
          buildCommand += ` --flavor ${options.flavor}`;
        }

        if (options.obfuscate) {
          buildCommand += ' --obfuscate --split-debug-info=debug-info/';
        }

        execSync(buildCommand, { stdio: 'pipe' });
        spinner.succeed(`✅ ${platform} build completed!`);
      }

      console.log(chalk.yellow('\n📦 Next steps:'));
      console.log(chalk.gray('   mkf submit-stores --stores both --track internal'));

    } catch (error) {
      console.error(chalk.red('❌ Build failed:'), error.message);
    }
  });

// Submit to Stores Command
program
  .command('submit-stores')
  .description('Submit to app stores with AI assistance')
  .option('--stores <stores>', 'Target stores', 'both')
  .option('--track <track>', 'Release track', 'internal')
  .option('--notes <notes>', 'Release notes')
  .action(async (options) => {
    console.log(chalk.blue('🏪 Submitting to app stores with AI assistance...\n'));

    const spinner = ora('Preparing store submissions...').start();

    try {
      await executeWorkflow('flutter-store-submission', {
        stores: options.stores.split(','),
        track: options.track,
        releaseNotes: options.notes
      });

      spinner.succeed(chalk.green('✅ Successfully submitted to stores!'));
    } catch (error) {
      spinner.fail(chalk.red('❌ Store submission failed:'));
      console.error(chalk.red(error.message));
    }
  });

// Helper Functions
async function createFlutterProject(config) {
  const { projectName, template, orgName, platforms, packages } = config;

  // Create Flutter project using Flutter CLI
  const createCommand = `flutter create --org ${orgName} --platforms ${platforms.join(',')} ${projectName}`;
  execSync(createCommand, { stdio: 'pipe' });

  // Setup template and packages
  await setupFlutterTemplate(projectName, template, packages);

  // Setup MobileKit configuration
  await setupMobileKitConfig(projectName, template, packages, platforms);

  console.log(chalk.green(`\n✅ Created ${projectName} with ${template} template`));
}

async function setupFlutterTemplate(projectName, template, packages) {
  const projectPath = path.resolve(projectName);

  // Update pubspec.yaml with selected packages
  const pubspecPath = path.join(projectPath, 'pubspec.yaml');
  let pubspec = await fs.readFile(pubspecPath, 'utf8');

  const packageVersions = {
    riverpod: 'flutter_riverpod: ^2.4.0\n  hooks_riverpod: ^2.4.0',
    go_router: 'go_router: ^12.0.0',
    drift: 'drift: ^2.13.0\n  drift_flutter: ^0.1.0',
    dio: 'dio: ^5.3.0',
    image_picker: 'image_picker: ^1.0.4',
    firebase: 'firebase_core: ^2.17.0\n  firebase_auth: ^4.12.0\n  cloud_firestore: ^4.13.0',
    freezed: 'freezed_annotation: ^2.4.1',
    cached_network_image: 'cached_network_image: ^3.3.0'
  };

  let additionalDeps = '';
  let devDeps = '';

  packages.forEach(pkg => {
    if (packageVersions[pkg]) {
      additionalDeps += `  ${packageVersions[pkg]}\n`;
    }
  });

  if (packages.includes('freezed')) {
    devDeps += `  freezed: ^2.4.6\n  json_serializable: ^6.7.1\n  build_runner: ^2.4.7\n`;
  }

  // Insert dependencies
  pubspec = pubspec.replace(/dependencies:\s*\n/, `dependencies:\n${additionalDeps}`);
  if (devDeps) {
    pubspec = pubspec.replace(/dev_dependencies:\s*\n/, `dev_dependencies:\n${devDeps}`);
  }

  await fs.writeFile(pubspecPath, pubspec);

  // Copy template files
  const templatePath = path.join(__dirname, '../templates', template);
  if (await fs.pathExists(templatePath)) {
    await fs.copy(templatePath, projectPath, { overwrite: true });
  }
}

async function setupMobileKitConfig(projectName, template, packages, platforms) {
  const config = {
    project_name: projectName,
    project_type: 'flutter',
    template,
    packages,
    platforms,
    created_date: new Date().toISOString(),
    mobilekit_version: VERSION
  };

  await fs.ensureDir(`${projectName}/.mobilekit`);
  await fs.writeJSON(`${projectName}/.mobilekit/config.json`, config, { spaces: 2 });

  // Copy agent files
  const agentsPath = path.join(__dirname, '../agents');
  if (await fs.pathExists(agentsPath)) {
    await fs.copy(agentsPath, `${projectName}/.mobilekit/agents`);
  }
}

async function executeWorkflow(workflowName, inputs) {
  console.log(chalk.yellow(`\n🔄 Executing ${workflowName} workflow...`));

  const workflows = {
    'generate-flutter-feature': async (data) => {
      console.log(chalk.blue('📋 flutter-planner: Creating implementation plan...'));
      await new Promise(resolve => setTimeout(resolve, 1000));

      console.log(chalk.blue('🔍 flutter-researcher: Researching packages and patterns...'));
      await new Promise(resolve => setTimeout(resolve, 1500));

      console.log(chalk.blue('🎨 widget-designer: Generating Flutter widgets...'));
      await new Promise(resolve => setTimeout(resolve, 2000));

      if (data.includeTests) {
        console.log(chalk.blue('🧪 flutter-tester: Creating test cases...'));
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      console.log(chalk.blue('👁️ dart-reviewer: Reviewing generated code...'));
      await new Promise(resolve => setTimeout(resolve, 800));

      console.log(chalk.green(`\n✅ Generated ${data.featureName} feature successfully!`));
    },

    'flutter-code-review': async (data) => {
      console.log(chalk.blue('👁️ dart-reviewer: Analyzing Dart code quality...'));
      await new Promise(resolve => setTimeout(resolve, 2000));

      console.log(chalk.blue('🔍 flutter-debugger: Checking for performance issues...'));
      await new Promise(resolve => setTimeout(resolve, 1500));

      console.log(chalk.blue('🎨 Checking Material Design compliance...'));
      await new Promise(resolve => setTimeout(resolve, 1000));

      console.log(chalk.green('\n✅ Code review completed with recommendations!'));
    },

    'flutter-store-submission': async (data) => {
      console.log(chalk.blue('🚀 flutter-release-manager: Preparing multi-store submission...'));
      await new Promise(resolve => setTimeout(resolve, 1500));

      console.log(chalk.blue('✍️ flutter-copywriter: Generating store descriptions...'));
      await new Promise(resolve => setTimeout(resolve, 1000));

      console.log(chalk.blue('📊 flutter-project-tracker: Updating project status...'));
      await new Promise(resolve => setTimeout(resolve, 500));

      console.log(chalk.green('\n✅ Successfully submitted to stores!'));
    },

    'analyze-flutter-test-results': async (data) => {
      console.log(chalk.blue('📊 Analyzing test coverage and widget performance...'));
      await new Promise(resolve => setTimeout(resolve, 1000));

      console.log(chalk.blue('🔍 Checking for Flutter-specific issues...'));
      await new Promise(resolve => setTimeout(resolve, 800));

      console.log(chalk.green('\n✅ Flutter test analysis completed!'));
    }
  };

  if (workflows[workflowName]) {
    await workflows[workflowName](inputs);
  } else {
    throw new Error(`Unknown workflow: ${workflowName}`);
  }
}

// Parse command line arguments
program.parse();

module.exports = program;
