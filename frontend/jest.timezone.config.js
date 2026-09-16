module.exports = {
  testEnvironment: 'node',
  testMatch: ['<rootDir>/tests/unit/office-time.spec.ts'],
  transform: {
    '^.+\\.tsx?$': ['ts-jest', { tsconfig: { esModuleInterop: true } }]
  }
}
