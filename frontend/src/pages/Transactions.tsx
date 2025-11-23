import { useState } from "react";
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
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";

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
  category: z.string().min(1, "Category is required"),
});

type TransactionForm = z.infer<typeof transactionSchema>;

const Transactions = () => {
  const [date, setDate] = useState<Date>();
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
  } = useForm<TransactionForm>({
    resolver: zodResolver(transactionSchema),
  });

  const onSubmit = (data: TransactionForm) => {
    console.log("Transaction data:", {
      ...data,
      amount: Number(data.amount),
    });
    
    toast.success("Transaction added successfully!", {
      description: `${data.type === "inflow" ? "Income" : "Expense"} of $${Number(data.amount).toLocaleString()} recorded.`,
    });
    
    reset();
    setDate(undefined);
  };

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
              <Label htmlFor="category">Category</Label>
              <Select onValueChange={(value) => setValue("category", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="revenue">Revenue</SelectItem>
                  <SelectItem value="operations">Operations</SelectItem>
                  <SelectItem value="payroll">Payroll</SelectItem>
                  <SelectItem value="marketing">Marketing</SelectItem>
                  <SelectItem value="utilities">Utilities</SelectItem>
                  <SelectItem value="consulting">Consulting</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
              {errors.category && (
                <p className="text-sm text-destructive">{errors.category.message}</p>
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

            <Button type="submit" className="w-full">
              Add Transaction
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default Transactions;
