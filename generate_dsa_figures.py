"""
Generate figures for DSA Report
==============================
Creates visualizations for all three modules' complexity analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Create output directory
OUTPUT_DIR = Path(__file__).parent / "plots" / "dsa_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


def plot_complexity_comparison():
    """Plot theoretical vs empirical complexity."""
    sizes = np.array([1000, 10000, 100000])
    
    # Theoretical complexities (normalized to n=1000)
    n = sizes
    o_1 = np.ones(3)  # O(1)
    o_log_n = np.log2(n) / np.log2(1000)  # O(log n)
    o_n = n / 1000  # O(n)
    o_n_log_n = (n * np.log2(n)) / (1000 * np.log2(1000))  # O(n log n)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(sizes))
    width = 0.2
    
    ax.bar(x - 1.5*width, o_1, width, label='O(1)', color='#2ecc71', alpha=0.8)
    ax.bar(x - 0.5*width, o_log_n, width, label='O(log n)', color='#3498db', alpha=0.8)
    ax.bar(x + 0.5*width, o_n, width, label='O(n)', color='#e74c3c', alpha=0.8)
    ax.bar(x + 1.5*width, o_n_log_n, width, label='O(n log n)', color='#9b59b6', alpha=0.8)
    
    ax.set_xlabel('Input Size (n)', fontsize=14)
    ax.set_ylabel('Relative Growth (normalized to n=1000)', fontsize=14)
    ax.set_title('Theoretical Time Complexity Comparison', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['10³', '10⁴', '10⁵'])
    ax.legend(loc='upper left', fontsize=12)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'complexity_comparison.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'complexity_comparison.pdf', bbox_inches='tight')
    print(f"✓ Saved: complexity_comparison.png/pdf")
    plt.close()


def plot_binary_search_comparisons():
    """Plot binary search comparisons vs log(n)."""
    sizes = [1000, 10000, 100000]
    avg_comparisons = [9.0, 12.4, 15.7]  # From benchmark output
    theoretical = [np.log2(n) for n in sizes]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(sizes))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, avg_comparisons, width, label='Actual Comparisons', 
                   color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, theoretical, width, label='log₂(n)', 
                   color='#2ecc71', alpha=0.8)
    
    ax.set_xlabel('Input Size (n)', fontsize=14)
    ax.set_ylabel('Number of Comparisons', fontsize=14)
    ax.set_title('Binary Search: Actual vs Theoretical Comparisons', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['10³', '10⁴', '10⁵'])
    ax.legend(fontsize=12)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'binary_search_analysis.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'binary_search_analysis.pdf', bbox_inches='tight')
    print(f"✓ Saved: binary_search_analysis.png/pdf")
    plt.close()


def plot_avl_tree_structure():
    """Create a visual representation of AVL tree."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Tree structure for sessions
    # Root: London (7-15)
    # Left: Asian (0-6)
    # Right: NewYork (13-21)
    
    nodes = [
        (50, 80, "London\n07:00-15:00", "#3498db"),  # Root
        (25, 50, "Asian\n00:00-06:00", "#2ecc71"),   # Left
        (75, 50, "NewYork\n13:00-21:00", "#e74c3c"), # Right
    ]
    
    # Draw edges
    ax.plot([50, 25], [75, 55], 'k-', linewidth=2)
    ax.plot([50, 75], [75, 55], 'k-', linewidth=2)
    
    # Draw nodes
    for x, y, label, color in nodes:
        circle = plt.Circle((x, y), 12, color=color, ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Add height annotations
    ax.text(50, 95, "Height = 2", ha='center', fontsize=14, fontweight='bold')
    ax.text(62, 80, "h=2", ha='center', fontsize=10, style='italic')
    ax.text(37, 50, "h=1", ha='center', fontsize=10, style='italic')
    ax.text(87, 50, "h=1", ha='center', fontsize=10, style='italic')
    
    ax.set_title('AVL Tree Structure: Trading Sessions\n(Balanced BST with O(log n) operations)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, color='#3498db', label='Root Node'),
        plt.Rectangle((0,0), 1, 1, color='#2ecc71', label='Left Child'),
        plt.Rectangle((0,0), 1, 1, color='#e74c3c', label='Right Child'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'avl_tree_structure.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'avl_tree_structure.pdf', bbox_inches='tight')
    print(f"✓ Saved: avl_tree_structure.png/pdf")
    plt.close()


def plot_heap_operations():
    """Plot MaxHeap operations timing."""
    sizes = [1000, 10000, 100000]
    insert_times = [1.602, 16.249, 202.797]  # From benchmark
    extract_times = [4.039, 61.449, 997.878]  # From benchmark
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(sizes))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, insert_times, width, label='Insert (O(log n))', 
                   color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, extract_times, width, label='Extract Max (O(log n))', 
                   color='#e74c3c', alpha=0.8)
    
    ax.set_xlabel('Input Size (n)', fontsize=14)
    ax.set_ylabel('Time (ms)', fontsize=14)
    ax.set_title('MaxHeap Operations: Insert vs Extract', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['10³', '10⁴', '10⁵'])
    ax.legend(fontsize=12)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'heap_operations.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'heap_operations.pdf', bbox_inches='tight')
    print(f"✓ Saved: heap_operations.png/pdf")
    plt.close()


def plot_dynamic_array_growth():
    """Plot dynamic array growth with doubling strategy."""
    # Simulate capacity growth
    capacities = [8]  # Initial capacity
    sizes = list(range(1, 101))  # Elements 1 to 100
    
    capacity_at_size = []
    current_cap = 8
    for size in sizes:
        if size > current_cap:
            current_cap *= 2
        capacity_at_size.append(current_cap)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(sizes, sizes, 'b-', linewidth=2, label='Array Size (n)')
    ax.plot(sizes, capacity_at_size, 'r--', linewidth=2, label='Capacity (doubling)')
    ax.fill_between(sizes, sizes, capacity_at_size, alpha=0.3, color='green', label='Unused Space')
    
    ax.set_xlabel('Number of Elements', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)
    ax.set_title('Dynamic Array: Doubling Strategy\nAmortized O(1) Insertion', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Mark resize points
    resize_points = [8, 16, 32, 64]
    for rp in resize_points:
        if rp <= 100:
            ax.axvline(x=rp, color='gray', linestyle=':', alpha=0.5)
            ax.annotate(f'Resize', xy=(rp, rp), xytext=(rp+2, rp+10),
                       fontsize=9, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dynamic_array_growth.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'dynamic_array_growth.pdf', bbox_inches='tight')
    print(f"✓ Saved: dynamic_array_growth.png/pdf")
    plt.close()


def plot_benchmark_summary():
    """Create summary benchmark chart."""
    operations = [
        'DynamicArray\nappend()',
        'Binary\nSearch',
        'AVL Tree\ninsert()',
        'AVL Tree\nsearch()',
        'LinkedList\ninsert()',
        'MaxHeap\ninsert()',
        'TradeManager\nadd_trade()'
    ]
    
    # Time per operation in microseconds for n=100,000
    times_100k = [0.155, 3.903, 9.667, 2.914, 1.368, 6.003, 3.257]
    
    # Expected complexity
    complexities = ['O(1)*', 'O(log n)', 'O(log n)', 'O(log n)', 'O(1)', 'O(log n)', 'O(log n)']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#2ecc71', '#3498db', '#3498db', '#3498db', '#2ecc71', '#3498db', '#3498db']
    bars = ax.barh(operations, times_100k, color=colors, alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Time per Operation (µs) at n=100,000', fontsize=14)
    ax.set_title('Benchmark Summary: Time per Operation', fontsize=16, fontweight='bold')
    
    # Add complexity labels
    for i, (bar, complexity) in enumerate(zip(bars, complexities)):
        width = bar.get_width()
        ax.annotate(complexity, xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', label='O(1) Constant'),
        Patch(facecolor='#3498db', label='O(log n) Logarithmic'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'benchmark_summary.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'benchmark_summary.pdf', bbox_inches='tight')
    print(f"✓ Saved: benchmark_summary.png/pdf")
    plt.close()


def plot_risk_heap_demo():
    """Visualize Max-Heap for risk management."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Before: Heap structure
    ax1 = axes[0]
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title('Max-Heap: Risk Priority Queue', fontsize=14, fontweight='bold')
    
    # Heap nodes (risk scores)
    heap_nodes = [
        (50, 85, "18.49\n(Highest)", "#e74c3c"),  # Root - max risk
        (30, 60, "6.24", "#f39c12"),
        (70, 60, "5.39", "#f39c12"),
        (15, 35, "2.86", "#3498db"),
        (45, 35, "2.38", "#3498db"),
        (55, 35, "1.52", "#2ecc71"),
    ]
    
    # Draw edges
    edges = [(50, 80, 30, 65), (50, 80, 70, 65), 
             (30, 55, 15, 40), (30, 55, 45, 40), (70, 55, 55, 40)]
    for x1, y1, x2, y2 in edges:
        ax1.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
    
    for x, y, label, color in heap_nodes:
        circle = plt.Circle((x, y), 10, color=color, ec='black', linewidth=2)
        ax1.add_patch(circle)
        ax1.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    ax1.text(50, 15, "Highest risk trade always at root\n→ O(1) peek, O(log n) extract", 
             ha='center', fontsize=11)
    
    # Right: Greedy removal visualization
    ax2 = axes[1]
    risks_before = [18.49, 6.24, 5.39, 2.86, 2.38, 1.52]
    risks_after = [6.24, 5.39, 2.86, 2.38, 1.52]  # After removing highest
    
    x = np.arange(6)
    ax2.bar(x, risks_before, color=['#e74c3c'] + ['#3498db']*5, alpha=0.5, label='Before', edgecolor='black')
    ax2.bar(x[:5], risks_after, color='#2ecc71', alpha=0.8, label='After removal', edgecolor='black', width=0.6)
    
    ax2.set_xlabel('Trade Index', fontsize=12)
    ax2.set_ylabel('Risk Score', fontsize=12)
    ax2.set_title('Greedy Risk Enforcement\n(Remove highest-risk trade)', fontsize=14, fontweight='bold')
    ax2.axhline(y=40, color='red', linestyle='--', label='Risk Budget')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'risk_heap_visualization.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'risk_heap_visualization.pdf', bbox_inches='tight')
    print(f"✓ Saved: risk_heap_visualization.png/pdf")
    plt.close()


def main():
    """Generate all figures for DSA report."""
    print("\n" + "=" * 60)
    print("  Generating DSA Report Figures")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}\n")
    
    plot_complexity_comparison()
    plot_binary_search_comparisons()
    plot_avl_tree_structure()
    plot_heap_operations()
    plot_dynamic_array_growth()
    plot_benchmark_summary()
    plot_risk_heap_demo()
    
    print("\n" + "=" * 60)
    print(f"✅ All figures saved to: {OUTPUT_DIR}")
    print("=" * 60)
    
    # List generated files
    print("\n📁 Generated files:")
    for f in sorted(OUTPUT_DIR.glob("*")):
        print(f"   • {f.name}")


if __name__ == "__main__":
    main()

