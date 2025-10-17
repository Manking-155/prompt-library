// Application Data
const agentsData = [
    {
        name: "Mobile Planner",
        id: "mobile-planner",
        description: "Plans mobile app architecture, UI/UX flow, and technical requirements",
        status: "active",
        icon: "📋",
        specialty: "Architecture & Planning"
    },
    {
        name: "Mobile Researcher",
        id: "mobile-researcher",
        description: "Researches Flutter packages, iOS frameworks, mobile best practices",
        status: "active",
        icon: "🔍",
        specialty: "Research & Analysis"
    },
    {
        name: "UI/UX Designer",
        id: "ui-ux-designer",
        description: "Generates UI mockups, converts to Flutter/SwiftUI code, creates assets",
        status: "active",
        icon: "🎨",
        specialty: "Design & Assets"
    },
    {
        name: "Database Architect",
        id: "database-architect",
        description: "Designs SQLite, CoreData schemas, offline storage strategies",
        status: "active",
        icon: "🗄️",
        specialty: "Data Management"
    },
    {
        name: "Mobile Tester",
        id: "mobile-tester",
        description: "Creates widget tests, integration tests, device compatibility tests",
        status: "active",
        icon: "🧪",
        specialty: "Quality Assurance"
    },
    {
        name: "Code Reviewer",
        id: "code-reviewer",
        description: "Reviews code for mobile best practices, performance, security",
        status: "active",
        icon: "👁️",
        specialty: "Code Quality"
    },
    {
        name: "Mobile Debugger",
        id: "mobile-debugger",
        description: "Analyzes crashes, performance issues, device-specific bugs",
        status: "active",
        icon: "🐛",
        specialty: "Debugging & Fixes"
    },
    {
        name: "Docs Manager",
        id: "docs-manager",
        description: "Maintains API docs, user guides, deployment instructions",
        status: "active",
        icon: "📚",
        specialty: "Documentation"
    },
    {
        name: "Git Manager",
        id: "git-manager",
        description: "Manages branches, releases, mobile-specific CI/CD workflows",
        status: "active",
        icon: "🌿",
        specialty: "Version Control"
    },
    {
        name: "Release Manager",
        id: "release-manager",
        description: "Handles App Store/Play Store releases, TestFlight deployments",
        status: "active",
        icon: "🚀",
        specialty: "Deployment"
    },
    {
        name: "Content Writer",
        id: "content-writer",
        description: "Creates app store descriptions, release notes, user communications",
        status: "active",
        icon: "✍️",
        specialty: "Content & Marketing"
    },
    {
        name: "Project Tracker",
        id: "project-tracker",
        description: "Tracks development progress, milestones, team coordination",
        status: "active",
        icon: "📊",
        specialty: "Project Management"
    }
];

const workflowsData = [
    {
        name: "New Feature Development",
        description: "Complete workflow for developing a new mobile feature",
        agents: ["mobile-planner", "mobile-researcher", "ui-ux-designer", "mobile-tester", "code-reviewer"]
    },
    {
        name: "Bug Fix & Release",
        description: "Workflow for identifying, fixing, and releasing bug fixes",
        agents: ["mobile-debugger", "mobile-tester", "code-reviewer", "git-manager", "release-manager"]
    },
    {
        name: "UI/UX Iteration",
        description: "Design iteration and implementation workflow",
        agents: ["ui-ux-designer", "mobile-tester", "code-reviewer", "docs-manager"]
    }
];

const commandsData = [
    {
        name: "mk new-project",
        description: "Initialize a new Flutter/iOS project with MobileKit setup"
    },
    {
        name: "mk generate-feature",
        description: "Generate a new feature with UI, tests, and documentation"
    },
    {
        name: "mk run-tests",
        description: "Run comprehensive test suite across devices"
    },
    {
        name: "mk review-code",
        description: "Trigger code review with mobile-specific checks"
    },
    {
        name: "mk build-release",
        description: "Build and prepare for App Store/Play Store release"
    },
    {
        name: "mk debug-crash",
        description: "Analyze and debug crash reports"
    }
];

const projectTypesData = [
    {
        name: "Flutter Cross-Platform",
        description: "Flutter app for iOS and Android",
        template: "flutter_template",
        icon: "📱"
    },
    {
        name: "iOS Native (Swift)",
        description: "Native iOS app using Swift and SwiftUI",
        template: "ios_swift_template",
        icon: "🍎"
    },
    {
        name: "React Native",
        description: "React Native cross-platform app",
        template: "react_native_template",
        icon: "⚛️"
    }
];

// Application State
let currentSection = 'dashboard';
let filteredAgents = [...agentsData];
let currentProjectType = null;
let currentWizardStep = 1;
let terminalHistory = [];
let historyIndex = -1;

// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const agentsGrid = document.getElementById('agents-grid');
const agentSearch = document.getElementById('agent-search');
const agentFilter = document.getElementById('agent-filter');
const workflowsList = document.getElementById('workflows-list');
const projectTypes = document.getElementById('project-types');
const terminalInput = document.getElementById('terminal-input');
const terminalOutput = document.getElementById('terminal-output');
const commandsList = document.getElementById('commands-list');

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    renderAgents();
    renderWorkflows();
    renderProjectTypes();
    renderCommands();
    initializeTerminal();
    initializeProjectWizard();
    initializeWorkflowBuilder();
    initializeQuickActions();
    initializeDocs();
});

// Navigation System
function initializeNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            switchSection(sectionId);
        });
    });
}

function switchSection(sectionId) {
    // Update active nav link
    navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('data-section') === sectionId);
    });
    
    // Update active section
    sections.forEach(section => {
        section.classList.toggle('active', section.id === sectionId);
    });
    
    currentSection = sectionId;
}

// Agents Management
function renderAgents() {
    agentsGrid.innerHTML = filteredAgents.map(agent => `
        <div class="agent-card" data-agent-id="${agent.id}">
            <div class="agent-header">
                <div class="agent-icon">${agent.icon}</div>
                <div class="agent-info">
                    <h4>${agent.name}</h4>
                    <span class="agent-specialty">${agent.specialty}</span>
                </div>
            </div>
            <p class="agent-description">${agent.description}</p>
            <div class="agent-status">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>Active</span>
                </div>
                <div class="agent-actions">
                    <button class="btn btn-sm btn-primary" onclick="configureAgent('${agent.id}')">Configure</button>
                    <button class="btn btn-sm btn-secondary" onclick="viewAgentLogs('${agent.id}')">Logs</button>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add search functionality
    if (agentSearch) {
        agentSearch.addEventListener('input', filterAgents);
    }
    
    // Add filter functionality
    if (agentFilter) {
        agentFilter.addEventListener('change', filterAgents);
    }
}

function filterAgents() {
    const searchTerm = agentSearch.value.toLowerCase();
    const filterSpecialty = agentFilter.value;
    
    filteredAgents = agentsData.filter(agent => {
        const matchesSearch = agent.name.toLowerCase().includes(searchTerm) || 
                            agent.description.toLowerCase().includes(searchTerm);
        const matchesFilter = filterSpecialty === 'all' || agent.specialty === filterSpecialty;
        
        return matchesSearch && matchesFilter;
    });
    
    renderAgents();
}

function configureAgent(agentId) {
    const agent = agentsData.find(a => a.id === agentId);
    alert(`Configuring ${agent.name}...\n\nThis would open the agent configuration panel.`);
}

function viewAgentLogs(agentId) {
    const agent = agentsData.find(a => a.id === agentId);
    addTerminalLine(`Viewing logs for ${agent.name}...`);
    addTerminalLine(`[INFO] Agent started successfully`);
    addTerminalLine(`[INFO] Processing 3 tasks in queue`);
    addTerminalLine(`[INFO] Last activity: 2 minutes ago`);
    switchSection('commands');
}

// Workflows Management
function renderWorkflows() {
    if (!workflowsList) return;
    
    workflowsList.innerHTML = workflowsData.map(workflow => `
        <div class="workflow-card">
            <div class="workflow-header">
                <h4>${workflow.name}</h4>
            </div>
            <p class="workflow-description">${workflow.description}</p>
            <div class="workflow-agents">
                ${workflow.agents.map(agentId => {
                    const agent = agentsData.find(a => a.id === agentId);
                    return `<span class="workflow-agent-tag">${agent ? agent.icon + ' ' + agent.name : agentId}</span>`;
                }).join('')}
            </div>
            <div class="workflow-actions">
                <button class="btn btn-sm btn-primary" onclick="runWorkflow('${workflow.name}')">Run</button>
                <button class="btn btn-sm btn-secondary" onclick="editWorkflow('${workflow.name}')">Edit</button>
            </div>
        </div>
    `).join('');
}

function runWorkflow(workflowName) {
    addTerminalLine(`Starting workflow: ${workflowName}`);
    addTerminalLine(`Initializing agents...`);
    setTimeout(() => {
        addTerminalLine(`✓ Workflow '${workflowName}' completed successfully`);
    }, 2000);
    switchSection('commands');
}

function editWorkflow(workflowName) {
    alert(`Editing workflow: ${workflowName}\n\nThis would open the workflow editor.`);
}

// Workflow Builder
function initializeWorkflowBuilder() {
    const createWorkflowBtn = document.getElementById('create-workflow');
    const closeBuilderBtn = document.getElementById('close-builder');
    const workflowBuilder = document.getElementById('workflow-builder');
    
    if (createWorkflowBtn) {
        createWorkflowBtn.addEventListener('click', () => {
            workflowBuilder.style.display = 'block';
            renderPaletteAgents();
        });
    }
    
    if (closeBuilderBtn) {
        closeBuilderBtn.addEventListener('click', () => {
            workflowBuilder.style.display = 'none';
        });
    }
}

function renderPaletteAgents() {
    const paletteAgents = document.getElementById('palette-agents');
    if (!paletteAgents) return;
    
    paletteAgents.innerHTML = agentsData.map(agent => `
        <div class="palette-agent" draggable="true" data-agent-id="${agent.id}">
            <span>${agent.icon}</span>
            <span>${agent.name}</span>
        </div>
    `).join('');
    
    // Add drag and drop functionality
    const agents = paletteAgents.querySelectorAll('.palette-agent');
    agents.forEach(agent => {
        agent.addEventListener('dragstart', handleDragStart);
    });
    
    const canvas = document.getElementById('workflow-canvas');
    if (canvas) {
        canvas.addEventListener('dragover', handleDragOver);
        canvas.addEventListener('drop', handleDrop);
    }
}

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.getAttribute('data-agent-id'));
}

function handleDragOver(e) {
    e.preventDefault();
}

function handleDrop(e) {
    e.preventDefault();
    const agentId = e.dataTransfer.getData('text/plain');
    const agent = agentsData.find(a => a.id === agentId);
    
    if (agent) {
        const canvas = e.target.closest('#workflow-canvas');
        const existingHint = canvas.querySelector('.canvas-hint');
        if (existingHint) existingHint.remove();
        
        const agentElement = document.createElement('div');
        agentElement.className = 'workflow-agent';
        agentElement.innerHTML = `
            <span>${agent.icon}</span>
            <span>${agent.name}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        agentElement.style.cssText = `
            position: absolute;
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius);
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            left: ${e.offsetX - 50}px;
            top: ${e.offsetY - 20}px;
            cursor: move;
        `;
        
        canvas.appendChild(agentElement);
    }
}

// Project Setup
function renderProjectTypes() {
    if (!projectTypes) return;
    
    projectTypes.innerHTML = projectTypesData.map(type => `
        <div class="project-type-card" data-template="${type.template}" onclick="selectProjectType('${type.template}')">
            <div class="project-type-icon">${type.icon}</div>
            <div class="project-type-name">${type.name}</div>
            <div class="project-type-description">${type.description}</div>
        </div>
    `).join('');
}

function selectProjectType(template) {
    // Remove previous selection
    document.querySelectorAll('.project-type-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    document.querySelector(`[data-template="${template}"]`).classList.add('selected');
    currentProjectType = template;
}

function initializeProjectWizard() {
    const wizardNext = document.getElementById('wizard-next');
    const wizardPrev = document.getElementById('wizard-prev');
    const createProjectBtn = document.getElementById('create-project');
    
    if (wizardNext) {
        wizardNext.addEventListener('click', () => {
            if (currentWizardStep === 1 && !currentProjectType) {
                alert('Please select a project type first.');
                return;
            }
            
            if (currentWizardStep < 2) {
                currentWizardStep++;
                updateWizardStep();
            }
        });
    }
    
    if (wizardPrev) {
        wizardPrev.addEventListener('click', () => {
            if (currentWizardStep > 1) {
                currentWizardStep--;
                updateWizardStep();
            }
        });
    }
    
    if (createProjectBtn) {
        createProjectBtn.addEventListener('click', createProject);
    }
}

function updateWizardStep() {
    document.querySelectorAll('.wizard-step').forEach((step, index) => {
        step.classList.toggle('active', index + 1 === currentWizardStep);
    });
    
    const wizardPrev = document.getElementById('wizard-prev');
    const wizardNext = document.getElementById('wizard-next');
    const createProjectBtn = document.getElementById('create-project');
    
    if (wizardPrev) wizardPrev.style.display = currentWizardStep > 1 ? 'block' : 'none';
    if (wizardNext) wizardNext.style.display = currentWizardStep < 2 ? 'block' : 'none';
    if (createProjectBtn) createProjectBtn.style.display = currentWizardStep === 2 ? 'block' : 'none';
}

function createProject() {
    const projectName = document.getElementById('project-name').value;
    const packageId = document.getElementById('package-id').value;
    const description = document.getElementById('project-description').value;
    
    if (!projectName || !packageId) {
        alert('Please fill in all required fields.');
        return;
    }
    
    addTerminalLine(`Creating new project: ${projectName}`);
    addTerminalLine(`Project type: ${currentProjectType}`);
    addTerminalLine(`Package ID: ${packageId}`);
    addTerminalLine(`Initializing project structure...`);
    
    setTimeout(() => {
        addTerminalLine(`✓ Project '${projectName}' created successfully!`);
        addTerminalLine(`📁 Project files generated in /projects/${projectName.toLowerCase().replace(/\s+/g, '-')}`);
    }, 2000);
    
    switchSection('commands');
}

// Terminal System
function initializeTerminal() {
    if (terminalInput) {
        terminalInput.addEventListener('keydown', handleTerminalInput);
    }
    
    const clearBtn = document.getElementById('clear-terminal');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearTerminal);
    }
    
    const helpBtn = document.getElementById('terminal-help');
    if (helpBtn) {
        helpBtn.addEventListener('click', showTerminalHelp);
    }
}

function handleTerminalInput(e) {
    if (e.key === 'Enter') {
        const command = e.target.value.trim();
        if (command) {
            executeCommand(command);
            terminalHistory.push(command);
            historyIndex = terminalHistory.length;
        }
        e.target.value = '';
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (historyIndex > 0) {
            historyIndex--;
            e.target.value = terminalHistory[historyIndex];
        }
    } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (historyIndex < terminalHistory.length - 1) {
            historyIndex++;
            e.target.value = terminalHistory[historyIndex];
        } else {
            historyIndex = terminalHistory.length;
            e.target.value = '';
        }
    }
}

function executeCommand(command) {
    addTerminalLine(`$ ${command}`, 'command');
    
    // Parse command
    const [cmd, ...args] = command.split(' ');
    
    switch (cmd) {
        case 'help':
            showTerminalHelp();
            break;
        case 'clear':
            clearTerminal();
            break;
        case 'mk':
            executeMobileKitCommand(args);
            break;
        case 'ls':
            addTerminalLine('agents/    workflows/    projects/    docs/');
            break;
        case 'status':
            addTerminalLine(`MobileKit v1.0.0`);
            addTerminalLine(`Active agents: ${agentsData.length}`);
            addTerminalLine(`Running workflows: 2`);
            addTerminalLine(`Projects: 8`);
            break;
        default:
            addTerminalLine(`Command not found: ${cmd}. Type 'help' for available commands.`);
    }
}

function executeMobileKitCommand(args) {
    const subcommand = args[0];
    
    switch (subcommand) {
        case 'new-project':
            addTerminalLine('Starting new project wizard...');
            setTimeout(() => switchSection('projects'), 1000);
            break;
        case 'generate-feature':
            addTerminalLine('Generating new feature...');
            addTerminalLine('📝 Creating feature files');
            addTerminalLine('🧪 Generating tests');
            addTerminalLine('📚 Updating documentation');
            setTimeout(() => {
                addTerminalLine('✅ Feature generated successfully!');
            }, 2000);
            break;
        case 'run-tests':
            addTerminalLine('Running test suite...');
            addTerminalLine('🧪 Widget tests: PASSED (24/24)');
            addTerminalLine('🧪 Integration tests: PASSED (12/12)');
            addTerminalLine('🧪 Unit tests: PASSED (86/86)');
            setTimeout(() => {
                addTerminalLine('✅ All tests passed!');
            }, 3000);
            break;
        case 'review-code':
            addTerminalLine('Starting code review...');
            addTerminalLine('👁️ Analyzing code quality');
            addTerminalLine('👁️ Checking mobile best practices');
            addTerminalLine('👁️ Scanning for security issues');
            setTimeout(() => {
                addTerminalLine('✅ Code review completed. No issues found.');
            }, 2500);
            break;
        case 'build-release':
            addTerminalLine('Building release version...');
            addTerminalLine('📦 Optimizing assets');
            addTerminalLine('📦 Building APK/IPA');
            addTerminalLine('📦 Signing release');
            setTimeout(() => {
                addTerminalLine('✅ Release build completed!');
            }, 4000);
            break;
        case 'debug-crash':
            addTerminalLine('Analyzing crash reports...');
            addTerminalLine('🐛 Processing stack traces');
            addTerminalLine('🐛 Identifying root cause');
            setTimeout(() => {
                addTerminalLine('🔍 Issue found: Null pointer exception in UserService.dart:42');
                addTerminalLine('💡 Suggested fix: Add null check before accessing user.profile');
            }, 2000);
            break;
        default:
            addTerminalLine(`Unknown MobileKit command: ${subcommand}`);
            addTerminalLine('Available commands: new-project, generate-feature, run-tests, review-code, build-release, debug-crash');
    }
}

function addTerminalLine(text, type = 'output') {
    if (!terminalOutput) return;
    
    const line = document.createElement('div');
    line.className = 'terminal-line';
    
    if (type === 'command') {
        line.innerHTML = `<span class="terminal-prompt">mobilekit@dev:~$</span><span class="terminal-text">${text.substring(2)}</span>`;
    } else {
        line.innerHTML = `<span class="terminal-text">${text}</span>`;
    }
    
    terminalOutput.appendChild(line);
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

function clearTerminal() {
    if (terminalOutput) {
        terminalOutput.innerHTML = `
            <div class="terminal-line">
                <span class="terminal-prompt">mobilekit@dev:~$</span>
                <span class="terminal-text">Terminal cleared</span>
            </div>
        `;
    }
}

function showTerminalHelp() {
    addTerminalLine('Available commands:');
    addTerminalLine('  help          - Show this help message');
    addTerminalLine('  clear         - Clear terminal');
    addTerminalLine('  ls            - List directories');
    addTerminalLine('  status        - Show MobileKit status');
    addTerminalLine('  mk <command>  - Execute MobileKit commands');
    addTerminalLine('');
    addTerminalLine('MobileKit commands:');
    commandsData.forEach(cmd => {
        addTerminalLine(`  ${cmd.name.padEnd(20)} - ${cmd.description}`);
    });
}

// Commands Reference
function renderCommands() {
    if (!commandsList) return;
    
    commandsList.innerHTML = commandsData.map(command => `
        <div class="command-item">
            <div>
                <div class="command-name">${command.name}</div>
                <div class="command-description">${command.description}</div>
            </div>
            <button class="btn btn-sm btn-primary" onclick="executeCommand('${command.name}')">Run</button>
        </div>
    `).join('');
}

// Quick Actions
function initializeQuickActions() {
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const action = e.currentTarget.getAttribute('data-action');
            handleQuickAction(action);
        });
    });
}

function handleQuickAction(action) {
    switch (action) {
        case 'new-project':
            switchSection('projects');
            break;
        case 'run-tests':
            executeCommand('mk run-tests');
            switchSection('commands');
            break;
        case 'review-code':
            executeCommand('mk review-code');
            switchSection('commands');
            break;
        case 'debug-crash':
            executeCommand('mk debug-crash');
            switchSection('commands');
            break;
    }
}

// Documentation System
function initializeDocs() {
    const docsLinks = document.querySelectorAll('.docs-link');
    const docsSections = document.querySelectorAll('.docs-section');
    
    docsLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('href').substring(1);
            
            // Update active link
            docsLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Update active section
            docsSections.forEach(section => {
                section.classList.toggle('active', section.id === sectionId);
            });
        });
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius);
        padding: 12px 16px;
        color: var(--text-primary);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;
document.head.appendChild(style);

// Mobile responsiveness
function handleMobileNavigation() {
    if (window.innerWidth <= 1024) {
        // Add mobile menu toggle functionality if needed
        // This would involve creating a hamburger menu and overlay
    }
}

// Listen for window resize
window.addEventListener('resize', handleMobileNavigation);

// Initialize mobile navigation on load
handleMobileNavigation();