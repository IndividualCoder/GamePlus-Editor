import subprocess

def check_aa_support():
    process = subprocess.Popen(["dxdiag", "/t"], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    aa_support = False
    for line in output.splitlines():
        if "Antialiasing" in line:
            aa_support = True
            break

    return aa_support

if __name__ == "__main__":
    print(check_aa_support())