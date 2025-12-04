import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2 } from "lucide-react";
import { useBusinessStore } from "@/stores/business-store";

const businessSchema = z.object({
  businessName: z
    .string()
    .trim()
    .min(1, "Business name is required")
    .max(100, "Business name must be less than 100 characters"),
  industry: z
    .string()
    .trim()
    .min(1, "Industry is required")
    .max(50, "Industry must be less than 50 characters"),
  currency: z
    .string()
    .trim()
    .min(1, "Currency is required")
    .max(10, "Currency must be less than 10 characters"),
  country: z
    .string()
    .trim()
    .min(1, "Country is required")
    .max(50, "Country must be less than 50 characters"),
  monthlyRevenue: z
    .string()
    .trim()
    .min(1, "Monthly revenue is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  monthlyExpenses: z
    .string()
    .trim()
    .min(1, "Monthly expenses are required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  currentCash: z
    .string()
    .trim()
    .min(1, "Current cash balance is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  outstandingDebt: z
    .string()
    .trim()
    .min(1, "Outstanding debt is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  employees: z
    .string()
    .trim()
    .min(1, "Number of employees is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0 && Number.isInteger(Number(val)), "Must be a whole number"),
  businessGoals: z
    .string()
    .trim()
    .max(500, "Business goals must be less than 500 characters")
    .optional(),
});

type BusinessForm = z.infer<typeof businessSchema>;

const CreateBusiness = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { createBusiness, fetchBusinesses } = useBusinessStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<BusinessForm>({
    resolver: zodResolver(businessSchema),
  });

  const onSubmit = async (data: BusinessForm) => {
    setIsSubmitting(true);
    try {
      const payload = {
        name: data.businessName,
        currency: data.currency,
        country: data.country,
        settings: {
          industry: data.industry,
          monthly_revenue: Number(data.monthlyRevenue),
          monthly_expenses: Number(data.monthlyExpenses),
          current_cash: Number(data.currentCash),
          outstanding_debt: Number(data.outstandingDebt),
          employees: Number(data.employees),
          goals: data.businessGoals,
        }
      };

      await createBusiness(payload);
      
      // Fetch updated list of businesses
      await fetchBusinesses();
      
      toast.success("Business created successfully!", {
        description: "Your new business has been added to your account.",
      });

      // Navigate to the business setup page for this new business
      navigate("/business-setup");
    } catch (error) {
      console.error("Business creation failed:", error);
      toast.error("Failed to create business", {
        description: "Please try again later.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Create New Business</h2>
          <p className="text-muted-foreground">
            Add a new business to your account for separate cashflow tracking and analysis.
          </p>
        </div>

        <Card className="p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="businessName">Business Name</Label>
                <Input
                  id="businessName"
                  placeholder="Your Business Inc."
                  {...register("businessName")}
                />
                {errors.businessName && (
                  <p className="text-sm text-destructive">{errors.businessName.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <Input
                  id="industry"
                  placeholder="e.g., Retail, SaaS, Consulting"
                  {...register("industry")}
                />
                {errors.industry && (
                  <p className="text-sm text-destructive">{errors.industry.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="currency">Currency</Label>
                <Input
                  id="currency"
                  placeholder="e.g., USD, EUR, GBP"
                  {...register("currency")}
                />
                {errors.currency && (
                  <p className="text-sm text-destructive">{errors.currency.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  placeholder="e.g., USA, UK, Canada"
                  {...register("country")}
                />
                {errors.country && (
                  <p className="text-sm text-destructive">{errors.country.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="monthlyRevenue">Average Monthly Revenue ($)</Label>
                <Input
                  id="monthlyRevenue"
                  type="number"
                  step="0.01"
                  placeholder="50000"
                  {...register("monthlyRevenue")}
                />
                {errors.monthlyRevenue && (
                  <p className="text-sm text-destructive">{errors.monthlyRevenue.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="monthlyExpenses">Average Monthly Expenses ($)</Label>
                <Input
                  id="monthlyExpenses"
                  type="number"
                  step="0.01"
                  placeholder="35000"
                  {...register("monthlyExpenses")}
                />
                {errors.monthlyExpenses && (
                  <p className="text-sm text-destructive">{errors.monthlyExpenses.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="currentCash">Current Cash Balance ($)</Label>
                <Input
                  id="currentCash"
                  type="number"
                  step="0.01"
                  placeholder="100000"
                  {...register("currentCash")}
                />
                {errors.currentCash && (
                  <p className="text-sm text-destructive">{errors.currentCash.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="outstandingDebt">Outstanding Debt ($)</Label>
                <Input
                  id="outstandingDebt"
                  type="number"
                  step="0.01"
                  placeholder="25000"
                  {...register("outstandingDebt")}
                />
                {errors.outstandingDebt && (
                  <p className="text-sm text-destructive">{errors.outstandingDebt.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="employees">Number of Employees</Label>
              <Input
                id="employees"
                type="number"
                placeholder="10"
                {...register("employees")}
              />
              {errors.employees && (
                <p className="text-sm text-destructive">{errors.employees.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="businessGoals">Business Goals (Optional)</Label>
              <Textarea
                id="businessGoals"
                placeholder="Describe your short-term and long-term business goals..."
                rows={4}
                {...register("businessGoals")}
              />
              {errors.businessGoals && (
                <p className="text-sm text-destructive">{errors.businessGoals.message}</p>
              )}
            </div>

            <div className="flex gap-4">
              <Button type="submit" className="flex-1" disabled={isSubmitting}>
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating Business...
                  </>
                ) : (
                  'Create Business'
                )}
              </Button>
              <Button type="button" variant="outline" onClick={() => reset()} disabled={isSubmitting}>
                Reset
              </Button>
            </div>
          </form>
        </Card>

        <Card className="p-6 mt-6 bg-primary/5 border-primary/20">
          <h3 className="font-semibold mb-2 flex items-center gap-2">
            <span className="text-primary">💡</span> Business Information
          </h3>
          <p className="text-sm text-muted-foreground">
            Creating a new business allows you to track its finances separately from your other businesses.
            All information is encrypted and secure.
          </p>
        </Card>
      </div>
    </div>
  );
};

export default CreateBusiness;