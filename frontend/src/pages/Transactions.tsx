import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { CalendarIcon, Loader2 } from "lucide-react";
import { format } from "date-fns";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { useBusinessStore } from "@/stores/business-store";

const transactionSchema = z.object({
  date: z.date({ required_error: "Date is required" }),
  description: z
    .string()
    .trim()
    .min(1, "Description is required")
    .max(200, "Description must be less than 200 characters"),
  amount: z
    .string()
    .trim()
    .min(1, "Amount is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) > 0, "Amount must be a positive number"),
  type: z.enum(["inflow", "outflow"], { required_error: "Transaction type is required" }),
  category_id: z.string().min(1, "Category is required"),
});

type TransactionForm = z.infer<typeof transactionSchema>;

interface Category {
  id: number;
  name: string;
  type: string;
}

const Transactions = () => {
  const [date, setDate] = useState<Date>();
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { currentBusiness } = useBusinessStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<TransactionForm>({
    resolver: zodResolver(transactionSchema),
  });

  const selectedType = watch("type");

  useEffect(() => {
    if (!currentBusiness) {
      setCategories([]);
      return;
    }

    const fetchCategories = async () => {
      setIsLoading(true);
      try {
        const response = await authenticatedRequest(`${API_ENDPOINTS.categories}?business_id=${currentBusiness.id}`);
        const data = await response.json();
        setCategories(data);
      } catch (error) {
        console.error("Failed to fetch categories:", error);
        toast.error("Failed to load categories");
      } finally {
        setIsLoading(false);
      }
    };

    fetchCategories();
  }, [currentBusiness]);

  const filteredCategories = categories.filter(cat => {
    if (!selectedType) return true;
    // Map transaction type to category type logic if needed, 
    // but for now assuming categories might be mixed or we just show all.
    // Ideally backend categories have 'income' or 'expense' types.
    // Let's filter if the category type matches.
    const typeMap: Record<string, string> = { inflow: 'income', outflow: 'expense' };
    return cat.type === typeMap[selectedType];
  });

  const onSubmit = async (data: TransactionForm) => {
    setIsSubmitting(true);
    try {
      const payload = {
        date: format(data.date, "yyyy-MM-dd"),
        description: data.description,
        amount: Number(data.amount),
        direction: data.type,
        category_id: Number(data.category_id),
        business_id: currentBusiness?.id,
      };

      await authenticatedRequest(API_ENDPOINTS.transactions, {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      toast.success("Transaction added successfully!", {
        description: `${data.type === "inflow" ? "Income" : "Expense"} of $${Number(data.amount).toLocaleString()} recorded.`,
      });

      reset();
      setDate(undefined);
      setValue("category_id", ""); // Reset select
    } catch (error) {
      console.error("Failed to create transaction:", error);
      toast.error("Failed to add transaction");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!currentBusiness) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6">
        <div className="max-w-2xl mx-auto">
          <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
            <div className="text-center">
              <p className="text-muted-foreground">Please select a business first or create one</p>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Add Transaction</h2>
          <p className="text-muted-foreground">
            Record your business income and expenses for accurate cashflow tracking.
          </p>
        </div>

        <Card className="p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="date">Transaction Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className="w-full justify-start text-left font-normal"
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {date ? format(date, "PPP") : <span>Pick a date</span>}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={(newDate) => {
                      setDate(newDate);
                      if (newDate) setValue("date", newDate);
                    }}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
              {errors.date && (
                <p className="text-sm text-destructive">{errors.date.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="type">Transaction Type</Label>
              <Select onValueChange={(value) => setValue("type", value as "inflow" | "outflow")}>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="inflow">Income (Cash In)</SelectItem>
                  <SelectItem value="outflow">Expense (Cash Out)</SelectItem>
                </SelectContent>
              </Select>
              {errors.type && (
                <p className="text-sm text-destructive">{errors.type.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="category_id">Category</Label>
              <Select onValueChange={(value) => setValue("category_id", value)} disabled={!selectedType || isLoading}>
                <SelectTrigger>
                  <SelectValue placeholder={isLoading ? "Loading..." : "Select category"} />
                </SelectTrigger>
                <SelectContent>
                  {filteredCategories.map((category) => (
                    <SelectItem key={category.id} value={category.id.toString()}>
                      {category.name}
                    </SelectItem>
                  ))}
                  {filteredCategories.length === 0 && !isLoading && (
                    <SelectItem value="no_categories" disabled>No categories found for this type</SelectItem>
                  )}
                </SelectContent>
              </Select>
              {errors.category_id && (
                <p className="text-sm text-destructive">{errors.category_id.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                placeholder="e.g., Client payment, Office supplies"
                {...register("description")}
              />
              {errors.description && (
                <p className="text-sm text-destructive">{errors.description.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="amount">Amount ($)</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                placeholder="0.00"
                {...register("amount")}
              />
              {errors.amount && (
                <p className="text-sm text-destructive">{errors.amount.message}</p>
              )}
            </div>

            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Adding Transaction...
                </>
              ) : (
                'Add Transaction'
              )}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default Transactions;
