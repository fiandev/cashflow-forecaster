import { useState, useEffect as ReactUseEffect } from "react";
import { useForm, Controller } from "react-hook-form";
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
import { SearchableSelect, type SearchableSelectItem } from "@/components/ui/searchable-select";

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

// Industry options for the searchable select
const industryOptions: SearchableSelectItem[] = [
  { value: "Technology", label: "Technology" },
  { value: "Healthcare", label: "Healthcare" },
  { value: "Finance", label: "Finance" },
  { value: "Retail", label: "Retail" },
  { value: "Manufacturing", label: "Manufacturing" },
  { value: "Consulting", label: "Consulting" },
  { value: "Real Estate", label: "Real Estate" },
  { value: "Education", label: "Education" },
  { value: "Hospitality", label: "Hospitality" },
  { value: "Transportation", label: "Transportation" },
  { value: "Agriculture", label: "Agriculture" },
  { value: "Construction", label: "Construction" },
  { value: "Energy", label: "Energy" },
  { value: "Entertainment", label: "Entertainment" },
  { value: "Insurance", label: "Insurance" },
  { value: "Media", label: "Media" },
  { value: "Telecommunications", label: "Telecommunications" },
  { value: "Automotive", label: "Automotive" },
  { value: "Food & Beverage", label: "Food & Beverage" },
  { value: "Pharmaceuticals", label: "Pharmaceuticals" },
  { value: "E-commerce", label: "E-commerce" },
  { value: "SaaS", label: "SaaS" },
  { value: "Non-profit", label: "Non-profit" },
  { value: "Other", label: "Other" },
];

const countryOptions: SearchableSelectItem[] = [
  { value: "USA", label: "United States" },
  { value: "GBR", label: "United Kingdom" },
  { value: "CAN", label: "Canada" },
  { value: "AUS", label: "Australia" },
  { value: "DEU", label: "Germany" },
  { value: "FRA", label: "France" },
  { value: "JPN", label: "Japan" },
  { value: "CHN", label: "China" },
  { value: "IND", label: "India" },
  { value: "BRA", label: "Brazil" },
  { value: "MEX", label: "Mexico" },
  { value: "ITA", label: "Italy" },
  { value: "ESP", label: "Spain" },
  { value: "NLD", label: "Netherlands" },
  { value: "CHE", label: "Switzerland" },
  { value: "SWE", label: "Sweden" },
  { value: "NOR", label: "Norway" },
  { value: "DNK", label: "Denmark" },
  { value: "SGP", label: "Singapore" },
  { value: "KOR", label: "South Korea" },
  { value: "ZAF", label: "South Africa" },
  { value: "NZL", label: "New Zealand" },
  { value: "RUS", label: "Russia" },
  { value: "TUR", label: "Turkey" },
  { value: "POL", label: "Poland" },
  { value: "CZE", label: "Czech Republic" },
  { value: "HUN", label: "Hungary" },
  { value: "ARG", label: "Argentina" },
  { value: "COL", label: "Colombia" },
  { value: "PER", label: "Peru" },
  { value: "CHL", label: "Chile" },
  { value: "VEN", label: "Venezuela" },
  { value: "EGY", label: "Egypt" },
  { value: "NGA", label: "Nigeria" },
  { value: "KEN", label: "Kenya" },
  { value: "GHA", label: "Ghana" },
  { value: "ETH", label: "Ethiopia" },
  { value: "MAR", label: "Morocco" },
  { value: "SAU", label: "Saudi Arabia" },
  { value: "ARE", label: "United Arab Emirates" },
  { value: "ISR", label: "Israel" },
  { value: "KAZ", label: "Kazakhstan" },
  { value: "AZE", label: "Azerbaijan" },
  { value: "PHL", label: "Philippines" },
  { value: "THA", label: "Thailand" },
  { value: "VNM", label: "Vietnam" },
  { value: "IDN", label: "Indonesia" },
  { value: "MYS", label: "Malaysia" },
  { value: "BRN", label: "Brunei" },
  { value: "KHM", label: "Cambodia" },
  { value: "LAO", label: "Laos" },
  { value: "MMR", label: "Myanmar" },
  { value: "TLS", label: "Timor-Leste" },
  { value: "IRL", label: "Ireland" },
  { value: "AUT", label: "Austria" },
  { value: "BEL", label: "Belgium" },
  { value: "PRT", label: "Portugal" },
  { value: "GRC", label: "Greece" },
];

// Currency options for the searchable select
const currencyOptions: SearchableSelectItem[] = [
  { value: "USD", label: "USD - US Dollar" },
  { value: "EUR", label: "EUR - Euro" },
  { value: "GBP", label: "GBP - British Pound" },
  { value: "JPY", label: "JPY - Japanese Yen" },
  { value: "CAD", label: "CAD - Canadian Dollar" },
  { value: "AUD", label: "AUD - Australian Dollar" },
  { value: "CHF", label: "CHF - Swiss Franc" },
  { value: "CNY", label: "CNY - Chinese Yuan" },
  { value: "INR", label: "INR - Indian Rupee" },
  { value: "MXN", label: "MXN - Mexican Peso" },
  { value: "SGD", label: "SGD - Singapore Dollar" },
  { value: "NZD", label: "NZD - New Zealand Dollar" },
  { value: "HKD", label: "HKD - Hong Kong Dollar" },
  { value: "NOK", label: "NOK - Norwegian Krone" },
  { value: "SEK", label: "SEK - Swedish Krona" },
  { value: "DKK", label: "DKK - Danish Krone" },
  { value: "PLN", label: "PLN - Polish Zloty" },
  { value: "CZK", label: "CZK - Czech Koruna" },
  { value: "HUF", label: "HUF - Hungarian Forint" },
  { value: "TRY", label: "TRY - Turkish Lira" },
  { value: "RUB", label: "RUB - Russian Ruble" },
  { value: "BRL", label: "BRL - Brazilian Real" },
  { value: "KRW", label: "KRW - South Korean Won" },
  { value: "ZAR", label: "ZAR - South African Rand" },
  { value: "IDR", label: "IDR - Indonesian Rupiah" },
  { value: "MYR", label: "MYR - Malaysian Ringgit" },
  { value: "THB", label: "THB - Thai Baht" },
  { value: "VND", label: "VND - Vietnamese Dong" },
  { value: "PHP", label: "PHP - Philippine Peso" },
  { value: "AED", label: "AED - UAE Dirham" },
  { value: "SAR", label: "SAR - Saudi Riyal" },
  { value: "CLP", label: "CLP - Chilean Peso" },
  { value: "EGP", label: "EGP - Egyptian Pound" },
  { value: "ISK", label: "ISK - Icelandic Króna" },
];

const BusinessSetup = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { currentBusiness, updateBusiness } = useBusinessStore();

  const {
    register,
    handleSubmit,
    control, // Add control for Controller component
    formState: { errors },
    reset,
    setValue, // Add setValue to update form fields
  } = useForm<BusinessForm>({
    resolver: zodResolver(businessSchema),
  });

  // Pre-populate form with current business data
  ReactUseEffect(() => {
    if (currentBusiness) {
      setValue('businessName', currentBusiness.name || '');
      setValue('currency', currentBusiness.currency || 'USD');
      setValue('country', currentBusiness.country || 'USA');
      if (currentBusiness.settings) {
        setValue('industry', currentBusiness.settings.industry || '');
        setValue('monthlyRevenue', currentBusiness.settings.monthly_revenue ? currentBusiness.settings.monthly_revenue.toString() : '');
        setValue('monthlyExpenses', currentBusiness.settings.monthly_expenses ? currentBusiness.settings.monthly_expenses.toString() : '');
        setValue('currentCash', currentBusiness.settings.current_cash ? currentBusiness.settings.current_cash.toString() : '');
        setValue('outstandingDebt', currentBusiness.settings.outstanding_debt ? currentBusiness.settings.outstanding_debt.toString() : '');
        setValue('employees', currentBusiness.settings.employees ? currentBusiness.settings.employees.toString() : '');
        setValue('businessGoals', currentBusiness.settings.goals || '');
      }
    }
  }, [currentBusiness, setValue]);

  if (!currentBusiness) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6">
        <div className="max-w-3xl mx-auto">
          <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
            <div className="text-center">
              <p className="text-muted-foreground">Please select a business first or create one</p>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  const onSubmit = async (data: BusinessForm) => {
    setIsSubmitting(true);
    try {
      // Update the existing business with new settings
      const payload = {
        name: data.businessName,
        currency: data.currency, // Use the selected currency from the form
        country: data.country, // Use the selected country from the form
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

      await updateBusiness(currentBusiness.id, payload);

      toast.success("Business profile saved!", {
        description: "Your business metrics have been updated successfully.",
      });

      navigate("/"); // Redirect to dashboard
    } catch (error) {
      console.error("Business setup failed:", error);
      toast.error("Failed to save business profile", {
        description: "Please try again later.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-full sm:max-w-3xl mx-auto">
        <div className="mb-6 sm:mb-8">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold mb-2">Business Setup</h2>
          <p className="text-sm sm:text-muted-foreground">
            Configure your business metrics for accurate AI-powered financial analysis.
          </p>
        </div>

        <Card className="p-4 sm:p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 sm:space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div className="space-y-2">
                <Label htmlFor="businessName">Business Name</Label>
                <Input
                  id="businessName"
                  placeholder="Your Business Inc."
                  {...register("businessName")}
                />
                {errors.businessName && (
                  <p className="text-xs sm:text-sm text-destructive">{errors.businessName.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <Controller
                  name="industry"
                  control={control}
                  render={({ field }) => (
                    <SearchableSelect
                      items={industryOptions}
                      value={field.value}
                      onValueChange={field.onChange}
                      placeholder="Select industry..."
                    />
                  )}
                />
                {errors.industry && (
                  <p className="text-xs sm:text-sm text-destructive">{errors.industry.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div className="space-y-2">
                <Label htmlFor="currency">Currency</Label>
                <Controller
                  name="currency"
                  control={control}
                  render={({ field }) => (
                    <SearchableSelect
                      items={currencyOptions}
                      value={field.value}
                      onValueChange={field.onChange}
                      placeholder="Select currency..."
                    />
                  )}
                />
                {errors.currency && (
                  <p className="text-xs sm:text-sm text-destructive">{errors.currency.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Controller
                  name="country"
                  control={control}
                  render={({ field }) => (
                    <SearchableSelect
                      items={countryOptions}
                      value={field.value}
                      onValueChange={field.onChange}
                      placeholder="Select country..."
                    />
                  )}
                />
                {errors.country && (
                  <p className="text-xs sm:text-sm text-destructive">{errors.country.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
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
                  <p className="text-xs sm:text-sm text-destructive">{errors.monthlyRevenue.message}</p>
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
                  <p className="text-xs sm:text-sm text-destructive">{errors.monthlyExpenses.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
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
                  <p className="text-xs sm:text-sm text-destructive">{errors.currentCash.message}</p>
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
                  <p className="text-xs sm:text-sm text-destructive">{errors.outstandingDebt.message}</p>
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
                <p className="text-xs sm:text-sm text-destructive">{errors.employees.message}</p>
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
                <p className="text-xs sm:text-sm text-destructive">{errors.businessGoals.message}</p>
              )}
            </div>

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
              <Button type="submit" className="w-full sm:flex-1" disabled={isSubmitting}>
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Saving...
                  </>
                ) : (
                  'Save Business Profile'
                )}
              </Button>
              <Button type="button" variant="outline" className="w-full sm:w-auto" onClick={() => reset()} disabled={isSubmitting}>
                Reset
              </Button>
            </div>
          </form>
        </Card>

        <Card className="p-4 sm:p-6 mt-4 sm:mt-6 bg-primary/5 border-primary/20">
          <h3 className="font-semibold mb-2 flex items-center gap-2">
            <span className="text-primary text-base">💡</span> Why we need this information
          </h3>
          <p className="text-sm sm:text-base text-muted-foreground">
            This data helps our AI analyze your financial health, predict cashflow patterns,
            and provide personalized risk assessments. All information is encrypted and secure.
          </p>
        </Card>
      </div>
    </div>
  );
};

export default BusinessSetup;
