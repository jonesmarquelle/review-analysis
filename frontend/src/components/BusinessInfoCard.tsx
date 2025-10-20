import React from 'react';

const BusinessInfoCard: React.FC<{ businessInfo: google.maps.places.Place | null }> = ({ businessInfo }) => {
  // Don't render if no business info
  if (!businessInfo) {
    return null;
  }

  return (
    <div className="mt-5 text-left bg-gray-700 p-5 rounded-lg w-4/5 max-w-4xl shadow-lg mb-5">
      <h2 className="text-2xl font-bold mb-4">Business Information</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Left Column - Basic Info */}
        <div>
            <h3 className="text-lg font-semibold text-blue-300 mb-2">
                {businessInfo.displayName || 'N/A'}
            </h3>
            
            <p className="text-sm text-gray-300 mb-1 truncate">
                <span className="font-medium">Category:</span> {businessInfo.types || 'N/A'}
            </p>
            
            <p className="text-sm text-gray-300 mb-1">
                <span className="font-medium">Overall Rating:</span> {
                    businessInfo.rating ? `${businessInfo.rating}/5` : 'N/A'
                }
            </p>
            
            <p className="text-sm text-gray-300 mb-1">
                <span className="font-medium">Total Reviews:</span> {
                    businessInfo.userRatingCount	 ? businessInfo.userRatingCount.toLocaleString() : 'N/A'
                }
            </p>
            <p className="text-sm text-gray-300 mb-1">
                <span className="font-medium">Place ID:</span> {businessInfo.id}
            </p>
        </div>
      </div>
    </div>
  );
};

export default BusinessInfoCard;