import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import psycopg2

# 1. Set up the local visualizer window and two sub-charts (ax1, ax2)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
fig.canvas.manager.set_window_title('Live Hardware Telemetry')

def get_latest_data(sensor_type):
    """Connects to PostgreSQL and fetches the 30 most recent readings."""
    conn = psycopg2.connect(
        host="localhost",
        database="iot_telemetry",
        user="vincentnguyen", 
        password="password"           
    )
    cur = conn.cursor()
    
    # Query the last 30 rows for the specific sensor, ordered by time
    cur.execute(f"""
        SELECT logged_at, reading_value 
        FROM sensor_logs 
        WHERE sensor_type = '{sensor_type}' 
        ORDER BY logged_at DESC 
        LIMIT 30;
    """)
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Reverse the rows so they graph chronologically (oldest on left, newest on right)
    rows.reverse()
    
    # Split the rows into two lists: one for timestamps (X-axis), one for values (Y-axis)
    times = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]
    
    return times, values

def update_graph(frame):
    """This function is called continuously to redraw the graphs."""
    # Fetch the latest data from the database
    cpu_times, cpu_values = get_latest_data('cpu_load_percent')
    ram_times, ram_values = get_latest_data('ram_usage_percent')
    
    # Clear and redraw the top CPU plot
    ax1.clear()
    ax1.plot(cpu_times, cpu_values, color='blue', linewidth=2, label='CPU Load (%)')
    ax1.set_ylim(0, 100)
    ax1.set_title('Real-Time CPU Load')
    ax1.set_ylabel('Percentage')
    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Clear and redraw the bottom RAM plot
    ax2.clear()
    ax2.plot(ram_times, ram_values, color='red', linewidth=2, label='RAM Usage (%)')
    ax2.set_ylim(0, 100)
    ax2.set_title('Real-Time RAM Usage')
    ax2.set_ylabel('Percentage')
    ax2.legend(loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Format the layout so the X-axis timestamps don't overlap
    plt.tight_layout()

# 2. Run the animation loop, updating the graph every 1000 milliseconds (1 second)
ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)

# 3. Open the local window
plt.show()
