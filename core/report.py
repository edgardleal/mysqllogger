
import os
from metadatabase import MetaDataBase
import template


if not os.path.exists("html"):
  os.makedirs("html")

class HtmlReport(object):
  """
    Generate an html report with collected data
  """

  def __init__(self):
    self.report_dir = "html"
    self.index = []
    self.template_path = path = os.path.dirname(template.__file__)

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

  def read_template(self, file_name):
    with open(self.template_path + "/" + file_name, "r") as f:
      result = f.read()
    return result

  def min_avg_max(self, array):
    """
      Return a tuple with 3 values representing
       min , avg , and max value
    """
    array.sort()
    total = len(array)
    _sum = sum(array)

    if total == 0:
      return [0, 0, 0]
    else:
      return [array[0], _sum / total , array[total - 1]]


  def executions_aggregated(self, field):
    """
      Return a list with scalar values
    """
    data = None
    with MetaDataBase() as m:
      cur = m.getCon().cursor()
      cur.execute("Select  count(*) as total from executions group by %s" % (field, ))
      data = cur.fetchall()
      cur.close()

    return map(lambda x: x[0], data)

  def generate_statistical(self):
    _html = self.read_template("statistic.tmp")
    data = []
    data += self.min_avg_max(self.executions_aggregated("minute"))
    data += self.min_avg_max(self.executions_aggregated("hour"))
    data += self.min_avg_max(self.executions_aggregated("day"))

    self.write_page("statistics.html", _html % tuple(data))


  def generate_queries(self):
    result = ""
    index = self.read_template("index.tmp")

    with MetaDataBase() as m:
      self.con = m.getCon()
      cur = self.con.cursor()
      cur.execute("""
      select q.id, q.sql, q.example, count(e.id)
        from queries q , executions e
         where e.query = q.id
         group by q.id, q.sql, q.example
         order by count(e.id) desc
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

  def generate(self):
    self.generate_queries()
    self.generate_statistical()
    print "Report generated in [%s]" % self.report_dir

