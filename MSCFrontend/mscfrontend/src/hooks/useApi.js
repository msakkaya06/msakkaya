import { useState } from "react";
import axios from "../api/axios";
import { useToast } from "../context/ToastContext";
import { extractMessage } from "../utils/apiErrors";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const { notify } = useToast();

  const request = async ({
    method = "GET",
    url,
    data = null,
    headers = {},
    notifyOnSuccess = true,
    silent = false,
  }) => {
    if (!silent) setLoading(true);
    try {
      const token = localStorage.getItem("access");
      const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios({
        method,
        url,
        data,
        headers: { ...headers, ...authHeaders },
      });

      if (notifyOnSuccess && response.data.message) {
        notify(response.data.message, "success");
      }

      return response.data;
    } catch (err) {
      notify(extractMessage(err), "error");
      throw err;
    } finally {
      if (!silent) setLoading(false);
    }
  };

  return { request, loading };
}
