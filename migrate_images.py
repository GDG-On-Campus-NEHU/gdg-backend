import sqlite3
import sys

print("=" * 60)
print("Database Migration: Removing Old Image Columns")
print("=" * 60)

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

def show_columns(table_name):
    """Display current columns"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = cursor.fetchall()
    print(f"\n{table_name} columns:")
    for col in cols:
        print(f"  - {col[1]} ({col[2]})")

# Show current state
print("\nCURRENT STATE:")
show_columns('landing_page_blogpost')
show_columns('landing_page_project')
show_columns('landing_page_teammember')

print("\n" + "=" * 60)
print("APPLYING CHANGES...")
print("=" * 60)

try:
    # BlogPost migration
    print("\n1. Migrating landing_page_blogpost...")
    cursor.execute("PRAGMA table_info(landing_page_blogpost)")
    cols = cursor.fetchall()
    has_image_url = any(col[1] == 'image_url' for col in cols)

    if not has_image_url:
        cursor.execute("ALTER TABLE landing_page_blogpost ADD COLUMN image_url VARCHAR(500) DEFAULT '' NOT NULL")
        print("   ✓ Added image_url column")
    else:
        print("   ✓ image_url column already exists")

    # Create new table without 'image' column
    cursor.execute("""
        CREATE TABLE landing_page_blogpost_new AS 
        SELECT id, title, summary, content, author_name, published_date, image_url
        FROM landing_page_blogpost
    """)
    cursor.execute("DROP TABLE landing_page_blogpost")
    cursor.execute("ALTER TABLE landing_page_blogpost_new RENAME TO landing_page_blogpost")
    print("   ✓ Removed old 'image' column")

    # Project migration
    print("\n2. Migrating landing_page_project...")
    cursor.execute("PRAGMA table_info(landing_page_project)")
    cols = cursor.fetchall()
    has_image_url = any(col[1] == 'image_url' for col in cols)

    if not has_image_url:
        cursor.execute("ALTER TABLE landing_page_project ADD COLUMN image_url VARCHAR(500) DEFAULT '' NOT NULL")
        print("   ✓ Added image_url column")
    else:
        print("   ✓ image_url column already exists")

    cursor.execute("""
        CREATE TABLE landing_page_project_new AS 
        SELECT id, title, description, content, author_name, published_date, image_url
        FROM landing_page_project
    """)
    cursor.execute("DROP TABLE landing_page_project")
    cursor.execute("ALTER TABLE landing_page_project_new RENAME TO landing_page_project")
    print("   ✓ Removed old 'image' column")

    # TeamMember migration
    print("\n3. Migrating landing_page_teammember...")
    cursor.execute("PRAGMA table_info(landing_page_teammember)")
    cols = cursor.fetchall()
    has_photo_url = any(col[1] == 'photo_url' for col in cols)

    if not has_photo_url:
        cursor.execute("ALTER TABLE landing_page_teammember ADD COLUMN photo_url VARCHAR(500) DEFAULT 'https://via.placeholder.com/150' NOT NULL")
        print("   ✓ Added photo_url column")
    else:
        print("   ✓ photo_url column already exists")

    cursor.execute("""
        CREATE TABLE landing_page_teammember_new AS 
        SELECT id, name, role, bio, skills, position_rank, 
               github_url, linkedin_url, instagram_url, twitter_url, website_url, photo_url
        FROM landing_page_teammember
    """)
    cursor.execute("DROP TABLE landing_page_teammember")
    cursor.execute("ALTER TABLE landing_page_teammember_new RENAME TO landing_page_teammember")
    print("   ✓ Removed old 'photo' column")

    conn.commit()

    print("\n" + "=" * 60)
    print("FINAL STATE:")
    print("=" * 60)
    show_columns('landing_page_blogpost')
    show_columns('landing_page_project')
    show_columns('landing_page_teammember')

    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
    sys.exit(1)
finally:
    conn.close()

