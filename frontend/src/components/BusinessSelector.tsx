import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { useBusinessStore } from "@/stores/business-store";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";

const BusinessSelector = () => {
  const {
    businesses,
    currentBusiness,
    fetchBusinesses,
    setCurrentBusiness,
    isLoading
  } = useBusinessStore();

  const navigate = useNavigate();

  useEffect(() => {
    // Fetch businesses when the component mounts
    fetchBusinesses();
  }, [fetchBusinesses]);

  const handleBusinessChange = (value: string) => {
    if (value === "create_new") {
      navigate("/create-business");
      return;
    }

    const businessId = parseInt(value);
    const selectedBusiness = businesses.find(b => b.id === businessId) || null;
    setCurrentBusiness(selectedBusiness);
  };

  const handleCreateBusiness = () => {
    navigate("/create-business");
  };

  if (isLoading && businesses.length === 0) {
    return (
      <Select disabled>
        <SelectTrigger className="w-[200px]">
          <SelectValue placeholder="Loading..." />
        </SelectTrigger>
      </Select>
    );
  }

  if (businesses.length === 0) {
    return (
      <div className="flex items-center gap-2">
        <Select disabled>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="No businesses" />
          </SelectTrigger>
        </Select>
        <Button variant="outline" size="sm" onClick={handleCreateBusiness}>
          <Plus className="h-4 w-4 mr-1" />
          New
        </Button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <Select
        value={currentBusiness ? currentBusiness.id.toString() : ""}
        onValueChange={handleBusinessChange}
      >
        <SelectTrigger className="w-[200px]">
          <SelectValue
            placeholder={currentBusiness ? currentBusiness.name : "Select Business"}
          />
        </SelectTrigger>
        <SelectContent>
          {businesses.map((business) => (
            <SelectItem
              key={business.id}
              value={business.id.toString()}
            >
              {business.name}
            </SelectItem>
          ))}
          <SelectItem value="create_new">
            <div className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Create New
            </div>
          </SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};

export default BusinessSelector;