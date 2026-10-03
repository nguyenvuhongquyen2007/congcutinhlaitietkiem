import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="tính lãi tiền gửi tiết kiệm_ Nguyễn Vũ Hồng Quyên",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP CÔNG CỤ TÍNH LÃI TIỀN GỬI TIẾT KIỆM_ NGUYỄN VŨ HỒNG QUYÊN ✨🌟💫")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi.")

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Thông tin tiền gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# TÍNH LÃI
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
    else:

        # Lãi suất dạng thập phân
        lai_suat_nam = lai_suat / 100

        # Tính tổng tiền lãi theo công thức lãi đơn
        # Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12
        tong_tien_lai = (
            tien_gui
            * lai_suat_nam
            * ky_han
            / 12
        )

        # =========================
        # TÍNH LÃI ĐỊNH KỲ
        # =========================

        if hinh_thuc == "Hàng tháng":

            so_ky = ky_han
            lai_dinh_ky = tong_tien_lai / so_ky

            ten_ky = "tháng"

        elif hinh_thuc == "Hàng quý":

            # Số quý trong kỳ hạn
            so_ky = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3,
            # vẫn tính phần lãi bình quân theo quý
            if so_ky == 0:
                so_ky = 1

            lai_dinh_ky = tong_tien_lai / (ky_han / 3)

            ten_ky = "quý"

        else:
            # Cuối kỳ nhận toàn bộ tiền lãi
            so_ky = 1
            lai_dinh_ky = tong_tien_lai
            ten_ky = "cuối kỳ"

        # Tổng số tiền cuối cùng
        tong_tien_nhan = tien_gui + tong_tien_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 KẾT QUẢ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                dinh_dang_tien(lai_dinh_ky)
            )

        with col2:
            st.metric(
                "📈 Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "💰 Tiền gốc",
                dinh_dang_tien(tien_gui)
            )

        with col4:
            st.metric(
                "🏦 Tổng tiền nhận được",
                dinh_dang_tien(tong_tien_nhan)
            )

        # =========================
        # CHI TIẾT
        # =========================

        st.subheader("📝 Chi tiết khoản gửi")

        st.write(f"**Số tiền gửi:** {dinh_dang_tien(tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

        if hinh_thuc == "Hàng tháng":
            st.info(
                f"Mỗi tháng nhận khoảng "
                f"**{dinh_dang_tien(lai_dinh_ky)}** tiền lãi."
            )

        elif hinh_thuc == "Hàng quý":
            st.info(
                f"Mỗi quý nhận khoảng "
                f"**{dinh_dang_tien(lai_dinh_ky)}** tiền lãi."
            )

        else:
            st.info(
                f"Cuối kỳ nhận "
                f"**{dinh_dang_tien(tong_tien_lai)}** tiền lãi."
            )

        st.caption(
            "Lưu ý: Kết quả trên sử dụng phương pháp tính lãi đơn, "
            "không tính lãi kép và chưa xét thuế/phí hoặc quy định riêng "
            "của từng ngân hàng."
        )
