import paramiko
import os

def login_server(hostname, username, key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file(key)
    ssh.connect(hostname=hostname,
                username=username, 
                pkey=k)
    print 'connected'
    return ssh

def copy_repo_2_server(ssh, repo):
    repo_name = os.path.basename(repo).split('.')[0]
    ssh.exec_command("rm -rf %s" % repo_name)  # delete if exists
    ssh.exec_command("git clone %s" % repo)   # git clone
    stdin, stdout, stderr = ssh.exec_command('ls')

    print 'Pull from Github successfully! Print the files in current directory:'
    print stdout.read().decode('utf-8')
    
def set_crontab(ssh, repo_path, script, prefix):
    # remove current crontab
    ssh.exec_command('crontab -r')

    # edd new crontab
    ssh.exec_command("echo '*/2 * * * * python " + repo_path + "/" + script + " " + prefix + "' > ~/crontabfile") 
    ssh.exec_command('crontab ~/crontabfile')

def deploy(key, hostname, prefix):
    ssh = login_server(hostname, 'testtest', key)
    copy_repo_2_server(ssh, 'https://github.com/weiwang0227/simple-service-n-deployment.git')
    ssh.exec_command('python '+'~/simple-service-n-deployment/process_json.py '+prefix)
    set_crontab(ssh, '~/simple-service-n-deployment', 'log_rotate.py', prefix)
    ssh.close() # log out  


if __name__ == '__main__':
    hostname = 'ec2-54-214-89-215.us-west-2.compute.amazonaws.com'
    username = 'testtest'
    key  = 'oregon.pem'
    deploy(key, hostname, 'prefix')
