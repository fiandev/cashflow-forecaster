import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2, Info } from "lucide-react";
import { useBusinessStore } from "@/stores/business-store";
import { formatCurrency } from "@/lib/utils";

interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  direction: "inflow" | "outflow";
  category_id: number;
  is_anomalous: boolean;
  business_id: number;
  ai_tag?: string;
}

interface Category {
  id: number;
  name: string;
  business_id: number;
}

export const TransactionsTable = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Record<number, string>>({});
  const [isLoading, setIsLoading] = useState(true);

  const { currentBusiness } = useBusinessStore();

  useEffect(() => {
    if (!currentBusiness) {
      // No business selected, clear data and show message
      setTransactions([]);
      setCategories({});
      setIsLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setIsLoading(true);

        // Fetch categories for the current business
        const categoriesResponse = await authenticatedRequest(`${API_ENDPOINTS.categories}?business_id=${currentBusiness.id}`);
        const categoriesData: Category[] = await categoriesResponse.json();
        const categoryMap = categoriesData.reduce((acc, cat) => {
          acc[cat.id] = cat.name;
          return acc;
        }, {} as Record<number, string>);
        setCategories(categoryMap);

        // Fetch transactions for the current business
        const transactionsResponse = await authenticatedRequest(`${API_ENDPOINTS.transactions}?business_id=${currentBusiness.id}`);
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
  }, [currentBusiness]);

  if (!currentBusiness) {
    return (
      <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Please select a business first or create one</p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  return (
    <Card className="p-4 sm:p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">Recent Transactions</h3>
      <div className="rounded-md border overflow-x-auto">
        <Table className="min-w-full">
          <TableHeader>
            <TableRow>
              <TableHead className="whitespace-nowrap">Date</TableHead>
              <TableHead className="whitespace-nowrap">Description</TableHead>
              <TableHead className="text-right whitespace-nowrap">Inflow</TableHead>
              <TableHead className="text-right whitespace-nowrap">Outflow</TableHead>
              <TableHead className="whitespace-nowrap hidden md:table-cell">Category</TableHead>
              <TableHead className="whitespace-nowrap hidden md:table-cell">AI Tag</TableHead>
              <TableHead className="whitespace-nowrap sm:hidden">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center text-muted-foreground">
                  No transactions found for this business.
                </TableCell>
              </TableRow>
            ) : (
              transactions.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell className="font-medium whitespace-nowrap">{transaction.date}</TableCell>
                  <TableCell className="max-w-[120px] sm:max-w-[200px] truncate" title={transaction.description}>
                    {transaction.description}
                  </TableCell>
                  <TableCell className="text-right text-success font-medium whitespace-nowrap">
                    {transaction.direction === "inflow" ? formatCurrency(transaction.amount, currentBusiness?.currency || 'USD') : "-"}
                  </TableCell>
                  <TableCell className="text-right text-destructive font-medium whitespace-nowrap">
                    {transaction.direction === "outflow" ? formatCurrency(transaction.amount, currentBusiness?.currency || 'USD') : "-"}
                  </TableCell>
                  <TableCell className="hidden md:table-cell whitespace-nowrap">{categories[transaction.category_id] || "Unknown"}</TableCell>
                  <TableCell className="hidden md:table-cell whitespace-nowrap">
                    {transaction.is_anomalous ? (
                      <Badge variant="destructive">
                        {transaction.ai_tag || "Anomalous"}
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="opacity-50">Normal</Badge>
                    )}
                  </TableCell>
                  <TableCell className="sm:hidden">
                    <div className="flex flex-col gap-1">
                      <div className="text-xs text-muted-foreground">Cat: {categories[transaction.category_id] || "Unknown"}</div>
                      <div>
                        {transaction.is_anomalous ? (
                          <Badge variant="destructive" className="text-xs">
                            {transaction.ai_tag || "Anomalous"}
                          </Badge>
                        ) : (
                          <Badge variant="secondary" className="opacity-50 text-xs">Normal</Badge>
                        )}
                      </div>
                    </div>
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
