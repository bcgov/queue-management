const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function renderProcessEnvironment(template) {
    return template.replace(/\{\{\s*\$processEnvironment\.([A-Z0-9_]+)\s*\}\}/g, (match, variableName) => {
        const value = process.env[variableName];

        if (value === undefined) {
            throw new Error(`Missing required environment variable: ${variableName}`);
        }

        return value;
    });
}

function main() {
    const [scriptFile, ...artilleryArgs] = process.argv.slice(2);

    if (!scriptFile) {
        throw new Error('Usage: node run-artillery.js <script-file> [artillery args]');
    }

    const sourcePath = path.resolve(__dirname, scriptFile);
    const source = fs.readFileSync(sourcePath, 'utf8');
    const rendered = renderProcessEnvironment(source);
    const renderedPath = path.join(
        path.dirname(sourcePath),
        `.artillery-${path.basename(scriptFile, path.extname(scriptFile))}-${process.pid}.yaml`
    );

    fs.writeFileSync(renderedPath, rendered);

    let result;
    try {
        result = spawnSync(
            'npx',
            ['artillery', 'run', ...artilleryArgs, renderedPath],
            {
                cwd: __dirname,
                env: process.env,
                stdio: 'inherit',
            }
        );
    } finally {
        fs.unlinkSync(renderedPath);
    }

    if (result.error) {
        throw result.error;
    }

    process.exit(result.status === null ? 1 : result.status);
}

main();
