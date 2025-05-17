import re

os_release_content = """
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.2 LTS"
PRETTY_NAME="Ubuntu 24.04.2 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.2 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
"""

lines = os_release_content.strip().split('\n')
combined = (
    lines[0] + lines[1].split('=')[0] + lines[2] + lines[3].split('=')[0] +
    lines[4].split('=')[0] + lines[5] + lines[6].split('=')[0] +
    lines[7].split('=')[0] + lines[8] + lines[9] + lines[10] +
    lines[11] + lines[12] + lines[13] + lines[14] + lines[15] + lines[16]
)

charset = sorted(list(set(combined + '0123456789')))
print(''.join(charset))