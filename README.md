# Key_Exchange_tpm2_tools_w_zeromq
Simple POC of RSA encrypt/decrypt on 2 separate devices using tpm2-tools and ZeroMq in python.
# Full scale project requirements:
- tpm2-tss
- tpm2-tools
- tpm-abrmd
- pyzmq
```
pip install pyzmq
```
# Optionally:
- Install IBM's TPM 2.0 TSS (for virtual TPM)
```diff
!For a more detailed explanation on installing and setting the Virtual TPM the following tutorial can be taken:
```
[https://github.com/terilenard/dias-logging/wiki/Setup-Virtual-TPM

# Hardware required:
- 2 devices on the same network 
# Running the scripts:
```
The project contains 2 python scripts, which should be runned on 2 separate devices with the requirements meeted. On one side the IP of the other device is required, on the other side the plain text of what is wanted to be encrypted, the encrypted text is then sent to the other device and decrypted.
```
# Tested on:
- Debian based distros
