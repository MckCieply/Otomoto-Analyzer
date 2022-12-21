#scrapper to remove old deals that are no longer listed
import sqlite3 as  sql
conn = sql.connect("otofeature/deals.db")
cur = conn.cursor()

def get_old(cur):
    query = cur.execute("SELECT id from cars")
    old_deals = [deal[0] for deal in query]
    return old_deals

def get_new(deal, new_deals = []):
    new_deals.append(deal)
    return new_deals

def check(new, old):
    to_remove = list(set(old) - set(new))
    return to_remove

def delete(conn, cur, to_remove):
    if not to_remove:
        print("There is nothing to remove")
    else:
        print("Removing...")
        for element in to_remove:
            print(f"{element}... ", end="")
            cur.execute('DELETE FROM cars WHERE id = ?', (element,))
            print("Done")
        conn.commit()

#gotta rework new to take whole list after scrapping is done
def main(conn, cur, old):
    get_old(cur)
    get_new()

