import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

interface Transaction {
  id: number;
  date: string;
  description: string;
  inflow: number;
  outflow: number;
  category: string;
  aiTag: "Normal" | "Unusual";
}

const transactions: Transaction[] = [
  {
    id: 1,
    date: "2025-01-20",
    description: "Client Payment - Invoice #1234",
    inflow: 15000,
    outflow: 0,
    category: "Revenue",
    aiTag: "Normal",
  },
  {
    id: 2,
    date: "2025-01-20",
    description: "Office Supplies",
    inflow: 0,
    outflow: 850,
    category: "Operations",
    aiTag: "Normal",
  },
  {
    id: 3,
    date: "2025-01-19",
    description: "Marketing Campaign",
    inflow: 0,
    outflow: 5200,
    category: "Marketing",
    aiTag: "Unusual",
  },
  {
    id: 4,
    date: "2025-01-19",
    description: "Subscription Revenue",
    inflow: 2400,
    outflow: 0,
    category: "Revenue",
    aiTag: "Normal",
  },
  {
    id: 5,
    date: "2025-01-18",
    description: "Payroll",
    inflow: 0,
    outflow: 12000,
    category: "Payroll",
    aiTag: "Normal",
  },
];

export const TransactionsTable = () => {
  return (
    <Card className="p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">Recent Transactions</h3>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Description</TableHead>
              <TableHead className="text-right">Inflow</TableHead>
              <TableHead className="text-right">Outflow</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>AI Tag</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell className="font-medium">{transaction.date}</TableCell>
                <TableCell>{transaction.description}</TableCell>
                <TableCell className="text-right text-success font-medium">
                  {transaction.inflow > 0 ? `$${transaction.inflow.toLocaleString()}` : "-"}
                </TableCell>
                <TableCell className="text-right text-destructive font-medium">
                  {transaction.outflow > 0 ? `$${transaction.outflow.toLocaleString()}` : "-"}
                </TableCell>
                <TableCell>{transaction.category}</TableCell>
                <TableCell>
                  <Badge variant={transaction.aiTag === "Unusual" ? "destructive" : "secondary"}>
                    {transaction.aiTag}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </Card>
  );
};
