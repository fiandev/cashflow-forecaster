import React from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Building2, Plus } from 'lucide-react';
import { useBusiness } from '@/contexts/BusinessContext';
import { useNavigate } from 'react-router-dom';

const BusinessSelector: React.FC = () => {
  const { 
    businesses, 
    currentBusiness, 
    setCurrentBusiness, 
    loading, 
    refreshBusinesses 
  } = useBusiness();
  const navigate = useNavigate();

  const handleBusinessChange = (business: Business) => {
    setCurrentBusiness(business);
    
    // Optionally, you can navigate to a relevant page for the selected business
    // For example, navigate to dashboard for the selected business
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button 
          variant="outline" 
          className="h-8 w-full justify-between gap-2"
          disabled={loading}
        >
          <div className="flex items-center gap-2">
            <Building2 className="h-4 w-4" />
            <span className="truncate max-w-[120px]">
              {loading 
                ? 'Loading...' 
                : currentBusiness 
                  ? currentBusiness.name 
                  : 'No business selected'}
            </span>
          </div>
          <svg
            className="h-4 w-4 shrink-0 text-muted-foreground"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="m6 9 6 6 6-6" />
          </svg>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel>Switch Business</DropdownMenuLabel>
        <DropdownMenuSeparator />
        
        {businesses.length > 0 ? (
          businesses.map((business) => (
            <DropdownMenuItem
              key={business.id}
              onClick={() => handleBusinessChange(business)}
              className={currentBusiness?.id === business.id ? 'bg-accent' : ''}
            >
              <div className="flex items-center gap-2">
                <Building2 className="h-4 w-4" />
                <div className="flex flex-col">
                  <span className="text-sm font-medium">{business.name}</span>
                  <span className="text-xs text-muted-foreground">{business.currency}</span>
                </div>
              </div>
            </DropdownMenuItem>
          ))
        ) : (
          <DropdownMenuItem disabled>No businesses found</DropdownMenuItem>
        )}
        
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => navigate('/business/new')}>
          <div className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            <span>Add Business</span>
          </div>
        </DropdownMenuItem>
        
        <DropdownMenuItem onClick={refreshBusinesses}>
          <div className="flex items-center gap-2">
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Refresh</span>
          </div>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default BusinessSelector;