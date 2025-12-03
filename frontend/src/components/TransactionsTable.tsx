import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2, Info } from "lucide-react";

interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  direction: "inflow" | "outflow";
  category_id: number;
  is_anomalous: boolean;
  ai_tag?: string;
}

interface Category {
  id: number;
  name: string;
}

export const TransactionsTable = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Record<number, string>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch categories first for mapping
        const categoriesResponse = await authenticatedRequest(API_ENDPOINTS.categories);
        const categoriesData: Category[] = await categoriesResponse.json();
        const categoryMap = categoriesData.reduce((acc, cat) => {
          acc[cat.id] = cat.name;
          return acc;
        }, {} as Record<number, string>);
        setCategories(categoryMap);

        // Fetch transactions
        const transactionsResponse = await authenticatedRequest(API_ENDPOINTS.transactions);
        const transactionsData: Transaction[] = await transactionsResponse.json();
        
        // Sort by date descending
        const sortedTransactions = transactionsData.sort((a, b) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        );
        
        setTransactions(sortedTransactions);
      } catch (error) {
        console.error("Failed to fetch transaction data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

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
            {transactions.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
                  No transactions found.
                </TableCell>
              </TableRow>
            ) : (
              transactions.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell className="font-medium">{transaction.date}</TableCell>
                  <TableCell>{transaction.description}</TableCell>
                  <TableCell className="text-right text-success font-medium">
                    {transaction.direction === "inflow" ? `$${transaction.amount.toLocaleString()}` : "-"}
                  </TableCell>
                  <TableCell className="text-right text-destructive font-medium">
                    {transaction.direction === "outflow" ? `$${transaction.amount.toLocaleString()}` : "-"}
                  </TableCell>
                  <TableCell>{categories[transaction.category_id] || "Unknown"}</TableCell>
                  <TableCell>
                    {transaction.is_anomalous ? (
                      <Badge variant="destructive">
                        {transaction.ai_tag || "Anomalous"}
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="opacity-50">Normal</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </Card>
  );
};
