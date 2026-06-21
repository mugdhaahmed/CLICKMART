import { X, Hash, Calendar, DollarSign, Package, MapPin } from "lucide-react";
import { useAxios } from "../hooks/useAxios";
import useAuth from "../hooks/useAuth";
import { useEffect, useState } from "react";

const OrderDetail = ({ orderId, isOpen, onClose }) => {

    const [order, setOrder] = useState(null)

     const { api } = useAxios();
     const { auth } = useAuth();

     useEffect(() => {
        if (!orderId) return
       const fetchOrders = async () => {
         try {
           const response = await api.get(`/orders/${orderId}`);
           setOrder(response.data);
         } catch (error) {
           console.error("Error fetching orders:", error);
         }
       };
       if (auth.accessToken) fetchOrders();
     }, [api, auth.accessToken, orderId]);

if (!order) return null;

    return (
        <>
            {/* Backdrop */}
            {isOpen && <div className="modal-backdrop fade show"></div>}

            {/* Modal */}
            <div
                className={`modal fade ${isOpen ? "show d-block" : ""}`}
                tabIndex="-1"
                style={{ backgroundColor: isOpen ? "rgba(0,0,0,0.2)" : "transparent" }}
            >
                <div className="modal-dialog modal-dialog-centered modal-lg">
                    <div className="modal-content border-0 shadow">
                        <div className="modal-header bg-light border-0">
                            <h5 className="modal-title fw-bold">Order Details</h5>
                            <button type="button" className="btn-close" onClick={onClose}></button>
                        </div>
                        <div className="modal-body p-4">
                            <div className="row g-4">
                                {/* Info Header */}
                                <div className="col-12 d-flex justify-content-between align-items-start border-bottom pb-3">
                                    <div>
                                        <div className="d-flex align-items-center gap-2 text-primary mb-1">
                                            <Hash size={16} />
                                            <span className="fw-bold">{order?.id}</span>
                                        </div>
                                        <div className="d-flex align-items-center gap-2 text-muted small">
                                            <Calendar size={14} />
                                            {new Date(order?.created_at).toLocaleDateString("en-GB")}
                                        </div>
                                    </div>
                                    <div className="text-end">
                                        <span className="badge rounded-pill bg-primary px-3 py-2">
                                            {order?.status}
                                        </span>
                                    </div>
                                </div>

                                {/* Totals Summary */}
                                <div className="col-md-6">
                                    <h6 className="fw-bold mb-3">Payment Summary</h6>
                                    <div className="bg-light p-3 rounded-3">
                                        <div className="d-flex justify-content-between mb-2">
                                            <span className="text-muted">Subtotal</span>
                                            <span>${order?.subtotal}</span>
                                        </div>
                                        <div className="d-flex justify-content-between mb-2">
                                            <span className="text-muted">Tax Amount</span>
                                            <span>${order?.tax_amount}</span>
                                        </div>
                                        <div className="d-flex justify-content-between fw-bold border-top pt-2">
                                            <span>Grand Total</span>
                                            <span className="text-primary">${order?.grand_total}</span>
                                        </div>
                                    </div>
                                </div>

                                {/* Delivery Info */}
                                <div className="col-md-6">
                                    <h6 className="fw-bold mb-3">Delivery Info</h6>
                                    <div className="d-flex gap-2 text-muted small">
                                        <MapPin size={16} className="flex-shrink-0" />
                                        <p>{order?.address}, {order?.city}, {order?.state}, {order?.zip_code}</p>
                                    </div>
                                    <p className="ms-2 text-muted small">{order?.phone}</p>
                                </div>

                                {/* Ordered Items */}
                                <div className="col-12">
                                    <h6 className="fw-bold mb-3 d-flex align-items-center gap-2">
                                        <Package size={16} /> Items
                                    </h6>
                                    <div className="table-responsive">
                                        <table className="table align-middle mb-0">
                                            <thead className="table-light">
                                                <tr>
                                                    <th>Product</th>
                                                    <th className="text-center">Qty</th>
                                                    <th className="text-end">Price</th>
                                                    <th className="text-end">Total</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {order?.items?.map((item) => (
                                                    <tr key={item?.id}>
                                                        <td>{item?.product_name}</td>
                                                        <td className="text-center">{item?.quantity}</td>
                                                        <td className="text-end">${item?.price}</td>
                                                        <td className="text-end">${item?.total_price}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </>
    );
};

export default OrderDetail;