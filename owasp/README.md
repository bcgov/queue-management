This example demonstrates how to analyze a simple Java project with Gradle.

Prerequisites
=============
* [SonarQube](http://www.sonarqube.org/downloads/) 4.5+
* [Gradle](http://www.gradle.org/) 2.1 or higher

Usage
=====
* Analyze the project with SonarQube using Gradle:

        gradle sonarqube [-Dsonar.host.url=... -Dsonar.jdbc.url=... -Dsonar.jdbc.username=... -Dsonar.jdbc.password=...]
