import time
import subprocess
import re

monitoring_interval = 0.2


def verify_mode_down():
    cmd = "ifconfig"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print("Error:", error)
        return []
    output_lines = output.split('\n')
    output_lines = filter(lambda x: x, output_lines)
    switch_process_list= {}
    for line in output_lines:
        print(line)
    return switch_process_list

# def main(pid_to_monitor):
    # start_time = time.time()
    # start_cpu_time = get_cpu_usage(pid_to_monitor)
    #
    # time.sleep(monitoring_interval)
    #
    # end_time = time.time()
    # end_cpu_time = get_cpu_usage(pid_to_monitor)
    #
    # cpu_usage_percentage = ((end_cpu_time - start_cpu_time) / (end_time - start_time))
    #
    # print("CPU avg: {:.2f}%".format(cpu_usage_percentage))
    # return cpu_usage_percentage

# if __name__ == "__main__":
#     pid_to_monitor = verify_mode_down()
