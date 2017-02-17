import argparse
import logging
import os
import xlrd
import csv


LOGGER = logging.getLogger(__name__)

def _configure_logging(args):
  log_format = "%(asctime)s - %(levelname)s - %(message)s"
  if args.quiet:
    level = logging.WARNING
  else:
    level = logging.INFO

  logging.basicConfig(level=level, format=log_format)


def _make_parser():
  parser = argparse.ArgumentParser()
  parser.description = "check the completeness, fixity, and content of a bag"
  parser.add_argument("-e", "--excel",
    help = "path to an AMI Excel file",
    required = True
  )
  parser.add_argument("-o", "--output",
    help = "relative path to output file",
    required = True
  )
  parser.add_argument('--quiet', action='store_true')
  return parser

def main():
  parser = _make_parser()
  args = parser.parse_args()

  _configure_logging(args)

  try:
    excel_path = os.path.abspath(args.excel)
    wb = xlrd.open_workbook(excel_path)
  except:
    LOGGER.error("{} is not path to a valid Excel workbook".format(args.excel))
    return

  LOGGER.info("Loaded Excel workbook {0} with sheets: {1}".format(
    os.path.split(excel_path)[1], ", ".join(wb.sheet_names())))

  issn_list = list()
  for sheet_name in wb.sheet_names():
    sheet = wb.sheet_by_name(sheet_name)

    pissn_col, eissn_col = None, None

    # first find the right columns
    for row in range(0, sheet.nrows):
      possible_header = sheet.row_values(row)
      if "ISSN" in possible_header and "eISSN" in possible_header:
        pissn_col = possible_header.index("ISSN")
        eissn_col = possible_header.index("eISSN")
        title_col = possible_header.index("Title")
        break
      if "P-ISSN" in possible_header and "E-ISSN" in possible_header:
        pissn_col = possible_header.index("P-ISSN")
        eissn_col = possible_header.index("E-ISSN")
        title_col = possible_header.index("Product title")
        break

    for data_row in range(row + 1, sheet.nrows):
      issn_data = [sheet.cell_value(data_row, pissn_col),
                   sheet.cell_value(data_row, eissn_col),
                   sheet.cell_value(data_row, title_col)]
      issn_list.append(issn_data)

  with open(args.output, 'w') as f:
    issn_csv = csv.writer(f, quoting=csv.QUOTE_ALL)
    issn_csv.writerow(["pISSN", "eISSN", "Title"])
    for row in issn_list:
      issn_csv.writerow(row)
    LOGGER.info("{0} rows written to {1}".format(
      len(issn_list), os.path.abspath(args.output)))





if __name__ == "__main__":
  main()
