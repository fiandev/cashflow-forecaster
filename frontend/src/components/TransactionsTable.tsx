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

interface TransactionsTableProps {
  transactions: Transaction[];
}

export const TransactionsTable = ({ transactions = [] }: TransactionsTableProps) => {
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
