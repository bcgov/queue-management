// Copyright 2022 Province of British Columbia
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

// Entry point for Cypress, set with the 'supportFile' configuration option.

// Import custom commands.

import './commands'

export const API_PREFIX = 'http://localhost:5000/api/v1/'
export const API_FEEDBACK_PREFIX = 'http://localhost:5001/api/v1/'
