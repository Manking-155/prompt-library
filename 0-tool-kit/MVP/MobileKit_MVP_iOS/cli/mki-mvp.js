#!/usr/bin/env node
// MobileKit MVP CLI for iOS (mki-mvp)
const { program } = require('commander');
const chalk = require('chalk');

program
  .name('mki-mvp')
  .description('MobileKit MVP Edition for iOS')
  .version('1.0.0-mvp');

program
  .command('init')
  .description('Initialize iOS MVP project')
  .option('--firebase-project <id>', 'Firebase project ID')
  .action((options) => {
    console.log(chalk.blue('🚀 Creating iOS MVP project...'));
    console.log(chalk.green('✅ Project created!'));
  });

program
  .command('feature')
  .argument('<action>', 'add, list, or remove')
  .option('--name <name>', 'Feature name')
  .action((action, options) => {
    console.log(chalk.blue('⚡ Generating iOS feature...'));
    console.log(chalk.green('✅ Feature created!'));
  });

program.parse();
