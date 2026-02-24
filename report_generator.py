import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ReportGenerator:

    BLACK = colors.black
    WHITE = colors.white
    LIGHT_GRAY = colors.HexColor("#EEEEEE")
    MID_GRAY = colors.HexColor("#AAAAAA")

    def __init__(self, output_folder="reports"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def generate(self, dashboard_data, month_name, year, transactions=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{month_name}_{year}_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        story = []
        story += self._build_header(month_name, year)
        story += self._build_revenue_section(dashboard_data["revenue_metrics"])
        story.append(Spacer(1, 12))
        story += self._build_top_products_section(dashboard_data["top_products"])
        story.append(Spacer(1, 12))
        story += self._build_inventory_section(dashboard_data["inventory_stats"], dashboard_data["stock_alerts"])
        story.append(Spacer(1, 12))
        story += self._build_transactions_section(transactions or [])
        story.append(Spacer(1, 12))
        story += self._build_footer()

        doc.build(story)
        return filepath

    def _styles(self):
        return {
            "title": ParagraphStyle("title", fontSize=18, textColor=self.BLACK,
                                    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4),
            "subtitle": ParagraphStyle("subtitle", fontSize=10, textColor=self.BLACK,
                                       fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4),
            "section": ParagraphStyle("section", fontSize=11, textColor=self.BLACK,
                                      fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4),
            "normal": ParagraphStyle("normal", fontSize=9, textColor=self.BLACK,
                                     fontName="Helvetica", spaceAfter=2),
            "footer": ParagraphStyle("footer", fontSize=8, textColor=self.BLACK,
                                     fontName="Helvetica", alignment=TA_CENTER),
        }

    def _table_style(self):
        return TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, self.BLACK),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [self.LIGHT_GRAY, self.WHITE]),
        ])

    def _build_header(self, month_name, year):
        s = self._styles()
        generated = datetime.now().strftime("%B %d, %Y %I:%M %p")
        return [
            Spacer(1, 6),
            Paragraph("Terminal 360", s["title"]),
            Paragraph("Point of Sale System", s["subtitle"]),
            Spacer(1, 4),
            HRFlowable(width="100%", thickness=1, color=self.BLACK, spaceAfter=8),
            Paragraph(f"Monthly Report - {month_name} {year}", s["section"]),
            Paragraph(f"Generated: {generated}", s["normal"]),
            Spacer(1, 8),
        ]

    def _build_revenue_section(self, metrics):
        s = self._styles()
        story = [
            Paragraph("Revenue Summary", s["section"]),
            HRFlowable(width="100%", thickness=0.5, color=self.BLACK, spaceAfter=6),
        ]

        data = [
            ["Metric", "Value"],
            ["Monthly Revenue", f"P{metrics['monthly_revenue']:,.2f}"],
            ["Total Transactions", str(metrics['monthly_transactions'])],
            ["Average Transaction", f"P{metrics['avg_transaction']:,.2f}"],
        ]

        table = Table(data, colWidths=[3.5 * inch, 3.5 * inch])
        table.setStyle(self._table_style())
        story.append(table)
        return story

    def _build_top_products_section(self, top_products):
        s = self._styles()
        story = [
            Paragraph("Top Selling Products", s["section"]),
            HRFlowable(width="100%", thickness=0.5, color=self.BLACK, spaceAfter=6),
        ]

        if not top_products:
            story.append(Paragraph("No sales data available for this month.", s["normal"]))
            return story

        data = [["Rank", "Product Name", "Units Sold", "Revenue"]]
        for idx, (name, info) in enumerate(top_products):
            data.append([
                str(idx + 1),
                name,
                str(info["quantity"]),
                f"P{info['revenue']:,.2f}",
            ])

        table = Table(data, colWidths=[0.6 * inch, 3.8 * inch, 1.1 * inch, 1.5 * inch])
        style = self._table_style()
        style.add("ALIGN", (1, 1), (1, -1), "LEFT")
        table.setStyle(style)
        story.append(table)
        return story

    def _build_inventory_section(self, stats, alerts):
        s = self._styles()
        story = [
            Paragraph("Inventory Overview", s["section"]),
            HRFlowable(width="100%", thickness=0.5, color=self.BLACK, spaceAfter=6),
        ]

        stat_data = [
            ["Total Products", "Total Stock", "Low Stock", "Out of Stock"],
            [
                str(stats["total_products"]),
                str(stats["total_stock"]),
                str(stats["low_stock_count"]),
                str(stats["out_of_stock_count"]),
            ],
        ]

        stat_table = Table(stat_data, colWidths=[1.75 * inch] * 4)
        stat_table.setStyle(self._table_style())
        story.append(stat_table)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Stock Alerts", s["section"]))

        alert_data = [["Status", "Alert"]]
        for alert in alerts:
            if alert["type"] == "critical":
                status = "OUT OF STOCK"
            elif alert["type"] == "warning":
                status = "LOW STOCK"
            else:
                status = "OK"
            alert_data.append([status, alert["message"]])

        alert_table = Table(alert_data, colWidths=[1.2 * inch, 5.8 * inch])
        style = self._table_style()
        style.add("ALIGN", (1, 1), (1, -1), "LEFT")
        alert_table.setStyle(style)
        story.append(alert_table)
        return story

    def _build_transactions_section(self, transactions):
        s = self._styles()
        story = [
            Paragraph("Transaction History", s["section"]),
            HRFlowable(width="100%", thickness=0.5, color=self.BLACK, spaceAfter=6),
        ]

        if not transactions:
            story.append(Paragraph("No transactions found for this month.", s["normal"]))
            return story

        data = [["Order ID", "Staff Name", "Items", "Amount", "Date"]]
        for t in transactions:
            if t.items and isinstance(t.items[0], dict):
                item_count = sum(item.get("quantity", 0) for item in t.items)
            else:
                item_count = sum(getattr(item, "quantity", 0) for item in t.items)

            data.append([
                t.order_id,
                t.staff_name,
                str(item_count),
                f"P{t.total_amount:,.2f}",
                t.date if hasattr(t, "date") and t.date else "",
            ])

        col_widths = [1.0 * inch, 1.5 * inch, 0.6 * inch, 1.2 * inch, 2.7 * inch]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        style = self._table_style()
        style.add("ALIGN", (1, 1), (1, -1), "LEFT")
        style.add("ALIGN", (4, 1), (4, -1), "LEFT")
        table.setStyle(style)
        story.append(table)
        return story

    def _build_footer(self):
        s = self._styles()
        return [
            Spacer(1, 8),
            HRFlowable(width="100%", thickness=0.5, color=self.BLACK, spaceAfter=4),
            Paragraph("Powered by Terminal 360 - Point of Sale System", s["footer"]),
        ]