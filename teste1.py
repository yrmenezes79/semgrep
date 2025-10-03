---
- name: Instalar Python3, pip e Semgrep
  hosts: all
  become: true
  tasks:
    - name: Instalar Python 3
      dnf:
        name: python3
        state: present
    - name: Instalar pip3
      dnf:
        name: python3-pip
        state: present
    - name: Instalar semgrep via pip3
      pip:
        name: semgrep
        executable: pip3
