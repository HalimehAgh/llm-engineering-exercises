import json
import sys

def fix_notebook(input_file):
    """
    Remove ALL widget metadata from a Jupyter notebook
    """
    print(f"🔧 Fixing notebook: {input_file}")
    
    try:
        # Read notebook
        with open(input_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        print("✓ Notebook loaded successfully")
        
        # Remove widgets from root metadata
        if 'metadata' in notebook and 'widgets' in notebook['metadata']:
            print("❌ Found 'widgets' in root metadata - REMOVING...")
            del notebook['metadata']['widgets']
            print("✅ Removed root-level widgets")
        
        # Remove widgets from each cell
        cells_fixed = 0
        for i, cell in enumerate(notebook.get('cells', [])):
            if 'metadata' in cell and 'widgets' in cell['metadata']:
                del cell['metadata']['widgets']
                cells_fixed += 1
        
        if cells_fixed > 0:
            print(f"✅ Removed widgets from {cells_fixed} cell(s)")
        
        # Save fixed notebook
        output_file = input_file.replace('.ipynb', '_FIXED.ipynb')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print(f"\n🎉 SUCCESS! Fixed notebook saved as:")
        print(f"   {output_file}")
        print(f"\n📤 Now upload this file to GitHub!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_notebook.py <notebook.ipynb>")
        print("\nOr drag and drop your notebook file onto this script!")
        
        # Try to find the notebook automatically
        import glob
        notebooks = glob.glob("*.ipynb")
        if notebooks:
            print(f"\nFound notebook(s): {notebooks}")
            print(f"Fixing first one: {notebooks[0]}")
            fix_notebook(notebooks[0])
        else:
            print("\nNo .ipynb files found in current directory")
    else:
        fix_notebook(sys.argv[1])