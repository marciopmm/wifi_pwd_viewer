import subprocess

def get_wifi_passwords():
    profiles_data = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
    profiles = []
    
    for line in profiles_data.split("\n"):
        if "Todos os Perfis de Usuário" in line or "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)

    wifi_info = []

    for profile in profiles:
        try:
            profile_data = subprocess.check_output(
                f'netsh wlan show profile name="{profile}" key=clear',
                shell=True, text=True
            )
            for line in profile_data.split("\n"):
                if "Conteúdo da Chave" in line or "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break
            else:
                password = "Sem senha ou não disponível"
            
            wifi_info.append((profile, password))
        except subprocess.CalledProcessError:
            wifi_info.append((profile, "Erro ao acessar o perfil"))

    return wifi_info

if __name__ == "__main__":
    for ssid, pwd in get_wifi_passwords():
        print(f"SSID: {ssid} | Senha: {pwd}")
