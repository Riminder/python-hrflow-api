<p align="center">
  <a href="https://hrflow.ai">
    <img alt="hrflow" src="https://img.riminder.net/logo-hrflow.svg" width="120" />
  </a>
</p>
<h1 align="center">
  HrFlow.ai Python SDK
</h1>
<p align="center">
    <em><b>Unify, Unleash, Automate Talent & Workforce Data</b></em>
</p>

<p align="center">
    <a href="https://github.com/Riminder/python-hrflow-api/stargazers/" target="_blank">
        <img src="https://img.shields.io/github/stars/riminder/python-hrflow-api?style=social" alt="Test">
    </a>
    <a href="https://pypi.org/project/hrflow/" target="_blank">
        <img src="https://img.shields.io/pypi/dm/hrflow">
    </a>
    <a href="https://github.com/riminder/python-hrflow-api/releases" target="_blank">
        <img src="https://img.shields.io/github/v/release/Riminder/python-hrflow-api" alt="Release">
    </a>
    <a href="https://join.slack.com/t/hrflow-club/shared_invite/zt-1qzbtkacg-pb7qhTyHAmditoKt_xPtSw" target="_blank">
        <img src="https://img.shields.io/badge/slack-join-white.svg?logo=slack" alt="Slack">
    </a>
    <a href="https://www.youtube.com/@hrflow.aiacademy9534/?sub_confirmation=1" target="_blank">
        <img alt="YouTube Channel Views" src="https://img.shields.io/youtube/channel/views/UCb6YzPCNnGEPTfrX-GmQyTg?style=social">
    </a>
    <a href="" target="_blank">
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white" alt="License">
    </a>
</p>

**HrFlow.ai** is the first System of Intelligence for Talent & Workforce Data, enabling leading AI-powered Talent & Workforce experiences. Our suite of APIs provide a suite of AI solutions to unleash clean, structured, normalized, updated and analyzed Talent Data with state-of-the-art seven AI modules. 

Furthermore, HrFlow.ai breaks data silos and creates a single source of truth (SSOT) for Talent Data. With our API connectors, businesses can sync data between their tools in milliseconds and build customizable workflows that meet their business logic. 

Our suite of APIs includes **Parsing API, Tagging API, Embedding API, Searching API, Scoring API, Imaging API**, and **OEM Widgets**. With our Automation Studio and AI Studio, businesses can utilize AI-powered user interfaces and **low-code/no-code** automations to create advanced custom user experiences.

## 💡 Help

See [documentation](Documentation.md) for more examples.

## 🛠️ Installation

Install using `pip install -U hrflow` or `conda install hrflow -c conda-forge`.

<p align="center">
  <a href="https://hrflow.ai">
    <img alt="hrflow" src="https://user-images.githubusercontent.com/57711045/223526020-af148489-1b64-44ed-9d1d-35814612d479.png" width=65% height=75% />
  </a>
</p>


## 🪄 Quick start

```py
from hrflow import Hrflow
client = Hrflow(api_secret="YOUR_API_KEY", api_user="YOU_USER_EMAIL")

# read file from directory (in binary mode) 
with open("path_to_file.pdf", "rb") as f:
    file = f.read()


#Parse it using this method without reference:
response = client.profile.parsing.add_file(
    source_key="INSERT_THE_TARGET_SOURCE_KEY",
    profile_file=file,
    sync_parsing=1, # This is to invoke real time parsing
    tags=[{"name": "application_reference", "value": "TS_X12345"}], # Attach an application tag to the profile to be parsed
)
```


## 📎 Resources
- [Slack](https://hrflow-club.slack.com/) for a speedy exchange of ideas between the Community and the HrFlow.ai team
- [HrFlow.ai Academy](https://www.youtube.com/@hrflow.aiacademy9534) on Youtube for videos on how to get started with HrFlow.ai
- [Updates page](https://updates.hrflow.ai/) to keep you informed about our product releases
- [Documentation](https://developers.hrflow.ai/reference/authentication) to provide information on HrFlow.ai features
- [Our Roadmap](https://roadmap.hrflow.ai/) to show upcoming features or request new ones
