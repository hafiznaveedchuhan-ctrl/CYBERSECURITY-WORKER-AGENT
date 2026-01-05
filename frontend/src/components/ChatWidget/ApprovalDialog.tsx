'use client';

interface ApprovalRequest {
  id: string;
  action: string;
  description: string;
  risk_level: string;
  status: 'pending' | 'approved' | 'rejected';
}

interface ApprovalDialogProps {
  approval: ApprovalRequest;
  onApprove: () => void;
  onReject: () => void;
  onClose: () => void;
}

const RISK_COLORS: Record<string, string> = {
  low: 'text-green-400 bg-green-900/30 border-green-600',
  medium: 'text-yellow-400 bg-yellow-900/30 border-yellow-600',
  high: 'text-orange-400 bg-orange-900/30 border-orange-600',
  critical: 'text-red-400 bg-red-900/30 border-red-600',
};

export function ApprovalDialog({
  approval,
  onApprove,
  onReject,
  onClose,
}: ApprovalDialogProps) {
  const riskColor = RISK_COLORS[approval.risk_level] || RISK_COLORS.medium;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg w-full max-w-md overflow-hidden border border-gray-700">
        {/* Header */}
        <div className="p-4 border-b border-gray-700 bg-yellow-900/20">
          <div className="flex items-center space-x-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-yellow-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <h3 className="text-lg font-semibold text-white">Action Requires Approval</h3>
          </div>
        </div>

        {/* Content */}
        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Requested Action
            </label>
            <p className="text-white font-medium">{approval.action}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Description
            </label>
            <p className="text-gray-300 text-sm">{approval.description}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Risk Level
            </label>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${riskColor}`}
            >
              {approval.risk_level.toUpperCase()}
            </span>
          </div>

          {/* Warning */}
          <div className="bg-gray-700/50 rounded-lg p-3 text-sm text-gray-300">
            <p className="flex items-start">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              This action requires human approval before execution. Please review carefully
              before approving.
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="p-4 border-t border-gray-700 flex space-x-3">
          <button
            onClick={onReject}
            className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            Reject
          </button>
          <button
            onClick={onApprove}
            className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Approve
          </button>
        </div>

        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
