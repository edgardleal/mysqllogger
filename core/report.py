
import os
from metadatabase import MetaDataBase


if not os.path.exists("html"):
  os.makedirs("html")

class HtmlReport:
  """
    Generate an html report with collected data
  """

  def __init__(self):
    self.report_dir = "html"
    self.index = []

  def write_page(self,file_name, html):
    with open(self.report_dir + "/" + file_name, 'w') as f:
      f.write(html)

  def html_by_query(self, record):
    return """
       <table border="1">
         <tr>
           <td>ID</td><td>{0}</td>
         </tr>
         <tr>
           <td>SQL</td><td>{1}</td>
         </tr>
         <tr>
            <td>Ex.</td>
            <td>{2}</td>
         </tr>
         <tr></tr>
         <tr>
            <td> <a href="index.html">Voltar</a> </td>
         </tr>
      </table>

    """.format(record[0], record[1], record[2])

  def generate_queries(self):
    result = ""
    index = """ <html><body><table border='1'>
       <thead>
       <tr>
         <th>ID</th>
         <th>Hits</th>
         <th>SQL</th>
        </tr>
        </thead>
    """
    with MetaDataBase() as m:
      self.con = m.getCon()
      cur = self.con.cursor()
      cur.execute("""
      select q.id, q.sql, q.example, count(e.id)
        from queries q , executions e
         where e.query = q.id
         group by q.id, q.sql, q.example
      """)
      data = cur.fetchall()
      j = 0
      for i in data:
        j += 1
        self.write_page("%d.html" % j,self.html_by_query(i))
        index += """
               <tr>
                 <td> <a href="{0}.html">{0}</a></td>
                 <td>{2}</td>
                 <td> {1}</td>
                </tr>
               """.format(j, i[1][:50], i[3])

      index += "</table></body></html>"
      self.write_page("index.html", index)
    return result

html = HtmlReport()
html.generate_queries()
