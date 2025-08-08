# In scripts/setup_local_env.py
import subprocess
import shlex
import sys
import time

def run_command(command, stream_output=True):
    """Executes a shell command, streams its output, and checks for errors."""
    print(f"🚀 Executing: {command}")
    try:
        # Use shlex.split to handle command arguments correctly and securely
        args = shlex.split(command)
        
        if not stream_output:
            # Use for commands where we only need the final result and exit code
            result = subprocess.run(args, capture_output=True, text=True, check=False)
            if result.returncode != 0 and "not found" not in result.stderr:
                # Print stderr only if it's not a simple "not found" error, which we handle
                print(f"   Warning: Command returned non-zero exit code. Stderr: {result.stderr.strip()}")
            return result

        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8'
        )

        # Stream the output in real-time
        for line in iter(process.stdout.readline, ''):
            print(f"   {line.strip()}")
        
        process.wait()
        
        if process.returncode != 0:
            print(f"❌ Error executing command: {command}")
            sys.exit(1)
            
    except FileNotFoundError:
        tool = command.split()[0]
        print(f"❌ Command '{tool}' not found. Is it installed and in your PATH?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

def create_k3d_cluster():
    """Creates a k3d cluster with specific settings for the project."""
    print("\n--- Creating k3d cluster 'redeploy-hub-local' ---")
    cluster_name = "redeploy-hub-local"
    
    # A more direct way to check if the cluster already exists
    check_command = f"k3d cluster get {cluster_name}"
    result = run_command(check_command, stream_output=False)
    
    if result.returncode == 0:
        print(f"✅ Cluster '{cluster_name}' already exists. Skipping creation.")
        return

    print(f"Cluster '{cluster_name}' not found. Creating a new one...")
    command = (
        f'k3d cluster create {cluster_name} '
        f'--api-port 6550 '
        f'-p "8080:80@loadbalancer" '
        f'--k3s-arg "--disable=traefik@server:0"'
    )
    run_command(command)
    print("   Waiting for cluster to become ready...")
    time.sleep(10)

def install_ingress_nginx():
    """Installs the NGINX ingress controller using Helm."""
    print("\n--- Installing ingress-nginx ---")
    
    # 1. Add the ingress-nginx Helm repository
    run_command("helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx")
    
    # 2. Update all Helm repositories
    run_command("helm repo update")
    
    # 3. Install the chart
    install_command = (
        "helm install ingress-nginx ingress-nginx/ingress-nginx "
        "--namespace ingress-nginx "
        "--create-namespace "
        "--wait"
    )
    run_command(install_command)

if __name__ == "__main__":
    print("Starting local environment setup...")
    
    create_k3d_cluster()
    install_ingress_nginx()
    
    print("\n" + "="*50)
    print("🎉 Local environment is ready!")
    print("="*50)
    print("You can verify the cluster status with:")
    print("  kubectl get nodes")
    print("\nAnd check the ingress controller with:")
    print("  kubectl get pods -n ingress-nginx")
    print("\nAccess services via http://localhost:8080")