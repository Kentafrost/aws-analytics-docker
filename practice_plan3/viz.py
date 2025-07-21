import matplotlib.pyplot as plt

# Data
labels = ['Windows', 'macOS', 'Linux', 'Other']
sizes = [70, 20, 5, 5]
colors = ['#0078D4', '#999999', '#FFA500', '#2BA640']  # Custom colors
explode = (0.1, 0, 0, 0)  # Explode Windows slice

# Create figure with a specific size
plt.figure(figsize=(10, 8))

# Create pie chart with customization
plt.pie(sizes, 
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

# Add title with custom styling
plt.title('Market Share of Operating Systems', pad=20, size=14, weight='bold')

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# Show the plot
plt.show()