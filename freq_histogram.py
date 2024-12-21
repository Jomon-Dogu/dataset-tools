import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

def read_indices_and_filter():
    """Reads the range of indices and an optional filter condition from user input."""
    while True:
        try:
            indices_input = input("Enter the range of indices with optional filter (e.g., [1:10] < 4000): ")
            
            # Extrahiere den Bereich der Indizes und die Bedingung
            if "[" in indices_input and "]" in indices_input:
                range_part = indices_input.split("]")[0][1:]  # Extrahiere den Bereich innerhalb [ ]
                condition_part = indices_input.split("]")[1].strip()  # Extrahiere die Bedingung
                
                start, end = map(int, range_part.split(":"))
                if condition_part:
                    operator, threshold = condition_part.split()
                    threshold = float(threshold)  # Konvertiere den Schwellwert in float
                    if operator not in ["<", ">", "<=", ">=", "==", "!="]:
                        raise ValueError("Invalid operator. Use one of: <, >, <=, >=, ==, !=")
                    return start, end, operator, threshold
                return start, end, None, None  # Keine Bedingung
            else:
                print("Invalid format. Please use the format [start:end] <threshold.")
        except Exception as e:
            print(f"Invalid input. Error: {e}. Please try again.")

def load_csv(csv_path):
    """Loads a CSV file and returns the DataFrame."""
    try:
        data = pd.read_csv(csv_path)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def select_column(data):
    """Prompts the user to select a column from the DataFrame."""
    print("\nAvailable columns:")
    for idx, col in enumerate(data.columns, start=1):
        print(f"{idx}: {col}")
    
    while True:
        try:
            col_index = int(input("Enter the number of the column you want to use: ")) - 1
            if 0 <= col_index < len(data.columns):
                return data.columns[col_index]
            else:
                print("Invalid selection. Please choose a valid column number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def apply_filter(values, operator, threshold):
    """Applies the filter condition to the values."""
    if operator == "<":
        return values[values < threshold]
    elif operator == ">":
        return values[values > threshold]
    elif operator == "<=":
        return values[values <= threshold]
    elif operator == ">=":
        return values[values >= threshold]
    elif operator == "==":
        return values[values == threshold]
    elif operator == "!=":
        return values[values != threshold]
    return values

def plot_histogram(values, filename="plot.png"):
    """Plots a histogram of the CPU frequencies."""
    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title("Distribution of Selected Values", fontsize=16)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Speichern als PNG-Datei
    plt.savefig(filename)
    print(f"Plot saved as {filename}.")
    plt.close()

def save_filtered_data(values, output_file="filtered_values.csv"):
    """Saves the filtered values to a CSV file."""
    filtered_data = pd.DataFrame(values, columns=["Filtered Values"])
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved as {output_file}.")

def main():
    # CSV-Pfad eingeben
    csv_path = input("Enter the path to the CSV file: ")
    data = load_csv(csv_path)
    if data is None:
        return
    
    # Benutzer wählt die Spalte aus
    selected_column = select_column(data)
    print(f"\nUsing column: {selected_column}")

    # Benutzereingabe für den Bereich der Zeilen und die Filterbedingung
    start, end, operator, threshold = read_indices_and_filter()

    # Wähle die Daten im angegebenen Bereich
    y_values = data.iloc[start:end][selected_column].to_numpy()  # Extrahiert die Werte der ausgewählten Spalte

    # Konvertiere die Werte in float (falls nötig)
    y_values = y_values.astype(float)

    # Wende die Bedingung an (falls vorhanden)
    if operator and threshold is not None:
        y_values = apply_filter(y_values, operator, threshold)
        print(f"Filtered values with condition '{operator} {threshold}': {len(y_values)} values remaining.")

    # Speichere die gefilterten Werte in einer CSV-Datei
    save_filtered_data(y_values, output_file="filtered_values.csv")

    # Erstelle das Histogramm
    plot_histogram(y_values, filename="filtered_values_histogram.png")

if __name__ == "__main__":
    main()
