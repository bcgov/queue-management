// vetur.config.js
//
// Added for the VSCode Vetur extension for Vue.js code. Without a file to
// describe where the Vue.js code resides, the extension will look in the root
// directory for package.json and tsconfig.json, and complain that they do not
// exist.
//
/** @type {import('vls').VeturConfig} */
module.exports = {
    // Notice: It only affects the settings used by Vetur.
    settings: {
        "vetur.experimental.templateInterpolationService": true
    },
    projects: [
        'appointment-frontend',
        {
            root: './appointment-frontend'
        },
        'frontend',
        {
            root: './frontend'
        }
    ]
}
