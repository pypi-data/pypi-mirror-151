#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/str.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/dict.hpp>
#include <pythonic/include/builtins/float_.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/exp.hpp>
#include <pythonic/include/numpy/linalg/norm.hpp>
#include <pythonic/include/numpy/log.hpp>
#include <pythonic/include/numpy/max.hpp>
#include <pythonic/include/numpy/min.hpp>
#include <pythonic/include/numpy/prod.hpp>
#include <pythonic/include/numpy/sqrt.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/pow.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/dict.hpp>
#include <pythonic/builtins/float_.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/exp.hpp>
#include <pythonic/numpy/linalg/norm.hpp>
#include <pythonic/numpy/log.hpp>
#include <pythonic/numpy/max.hpp>
#include <pythonic/numpy/min.hpp>
#include <pythonic/numpy/prod.hpp>
#include <pythonic/numpy/sqrt.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/pow.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__rbfinterp_pythran
{
  struct polynomial_matrix
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::prod{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type5;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type5>::type>::type __type6;
      typedef decltype(std::declval<__type3>()(std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef __type8 __type9;
      typedef decltype(std::declval<__type2>()[std::declval<__type9>()]) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type11;
      typedef __type11 __type12;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type12>())) __type14;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type14>::type>::type __type15;
      typedef decltype(std::declval<__type3>()(std::declval<__type15>())) __type16;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
      typedef __type17 __type18;
      typedef decltype(std::declval<__type12>()[std::declval<__type18>()]) __type19;
      typedef decltype(pythonic::builtins::pow(std::declval<__type10>(), std::declval<__type19>())) __type20;
      typedef decltype(std::declval<__type0>()(std::declval<__type20>())) __type21;
      typedef __type21 __type22;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type18>())) __type25;
      typedef __type25 __type26;
      typedef pythonic::types::none_type __type27;
      typedef typename pythonic::returnable<__type27>::type __type28;
      typedef __type22 __ptype0;
      typedef __type26 __ptype1;
      typedef __type28 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& x, argument_type1&& powers, argument_type2&& out) const
    ;
  }  ;
  struct kernel_matrix
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::linalg::functor::norm{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef __type3 __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type4>())) __type7;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type __type8;
      typedef decltype(std::declval<__type5>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef __type10 __type11;
      typedef decltype(std::declval<__type4>()[std::declval<__type11>()]) __type12;
      typedef long __type15;
      typedef decltype(pythonic::operator_::add(std::declval<__type11>(), std::declval<__type15>())) __type16;
      typedef decltype(std::declval<__type5>()(std::declval<__type16>())) __type17;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type17>::type::iterator>::value_type>::type __type18;
      typedef __type18 __type19;
      typedef decltype(std::declval<__type4>()[std::declval<__type19>()]) __type20;
      typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type20>())) __type21;
      typedef decltype(std::declval<__type2>()(std::declval<__type21>())) __type22;
      typedef decltype(std::declval<__type1>()(std::declval<__type22>())) __type23;
      typedef __type23 __type24;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type19>())) __type27;
      typedef __type27 __type28;
      typedef pythonic::types::none_type __type29;
      typedef typename pythonic::returnable<__type29>::type __type30;
      typedef __type24 __ptype4;
      typedef __type28 __ptype5;
      typedef __type30 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& x, argument_type1&& kernel_func, argument_type2&& out) const
    ;
  }  ;
  struct polynomial_vector
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::prod{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef __type3 __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type4>())) __type7;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type __type8;
      typedef decltype(std::declval<__type5>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef __type10 __type11;
      typedef decltype(std::declval<__type4>()[std::declval<__type11>()]) __type12;
      typedef decltype(pythonic::builtins::pow(std::declval<__type2>(), std::declval<__type12>())) __type13;
      typedef decltype(std::declval<__type0>()(std::declval<__type13>())) __type14;
      typedef __type14 __type15;
      typedef __type11 __type17;
      typedef pythonic::types::none_type __type18;
      typedef typename pythonic::returnable<__type18>::type __type19;
      typedef __type15 __ptype12;
      typedef __type17 __ptype13;
      typedef __type19 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& x, argument_type1&& powers, argument_type2&& out) const
    ;
  }  ;
  struct kernel_vector
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::linalg::functor::norm{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef __type3 __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type5;
      typedef __type5 __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type7;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type6>())) __type9;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
      typedef decltype(std::declval<__type7>()(std::declval<__type10>())) __type11;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
      typedef __type12 __type13;
      typedef decltype(std::declval<__type6>()[std::declval<__type13>()]) __type14;
      typedef decltype(pythonic::operator_::sub(std::declval<__type4>(), std::declval<__type14>())) __type15;
      typedef decltype(std::declval<__type2>()(std::declval<__type15>())) __type16;
      typedef decltype(std::declval<__type1>()(std::declval<__type16>())) __type17;
      typedef __type17 __type18;
      typedef __type13 __type20;
      typedef pythonic::types::none_type __type21;
      typedef typename pythonic::returnable<__type21>::type __type22;
      typedef __type18 __ptype16;
      typedef __type20 __ptype17;
      typedef __type22 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& x, argument_type1&& y, argument_type2&& kernel_func, argument_type3&& out) const
    ;
  }  ;
  struct gaussian
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::exp{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(std::declval<__type1>()(std::declval<__type3>())) __type4;
      typedef decltype(pythonic::operator_::neg(std::declval<__type4>())) __type5;
      typedef decltype(std::declval<__type0>()(std::declval<__type5>())) __type6;
      typedef typename pythonic::returnable<__type6>::type __type7;
      typedef __type7 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct inverse_quadratic
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef long __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(std::declval<__type1>()(std::declval<__type3>())) __type4;
      typedef decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type0>())) __type5;
      typedef decltype(pythonic::operator_::div(std::declval<__type0>(), std::declval<__type5>())) __type6;
      typedef typename pythonic::returnable<__type6>::type __type7;
      typedef __type7 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct inverse_multiquadric
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef long __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef __type3 __type4;
      typedef decltype(std::declval<__type2>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type5>(), std::declval<__type0>())) __type6;
      typedef decltype(std::declval<__type1>()(std::declval<__type6>())) __type7;
      typedef decltype(pythonic::operator_::div(std::declval<__type0>(), std::declval<__type7>())) __type8;
      typedef typename pythonic::returnable<__type8>::type __type9;
      typedef __type9 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct multiquadric
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(std::declval<__type1>()(std::declval<__type3>())) __type4;
      typedef long __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(std::declval<__type0>()(std::declval<__type6>())) __type7;
      typedef decltype(pythonic::operator_::neg(std::declval<__type7>())) __type8;
      typedef typename pythonic::returnable<__type8>::type __type9;
      typedef __type9 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct quintic
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>())) __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type3>())) __type4;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type2>())) __type6;
      typedef decltype(pythonic::operator_::neg(std::declval<__type6>())) __type7;
      typedef typename pythonic::returnable<__type7>::type __type8;
      typedef __type8 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct cubic
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>())) __type3;
      typedef decltype(pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type2>())) __type5;
      typedef typename pythonic::returnable<__type5>::type __type6;
      typedef __type6 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct thin_plate_spline
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(std::declval<__type1>()(std::declval<__type3>())) __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type5;
      typedef decltype(std::declval<__type5>()(std::declval<__type3>())) __type7;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type7>())) __type8;
      typedef typename __combined<__type0,__type8>::type __type9;
      typedef typename pythonic::returnable<__type9>::type __type10;
      typedef __type10 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct linear
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef decltype(pythonic::operator_::neg(std::declval<__type1>())) __type2;
      typedef typename pythonic::returnable<__type2>::type __type3;
      typedef __type3 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& r) const
    ;
  }  ;
  struct _polynomial_matrix
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
      typedef __type6 __type7;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type7>())) __type8;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>(), std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type11;
      typedef decltype(std::declval<__type0>()(std::declval<__type10>(), std::declval<__type11>())) __type12;
      typedef typename pythonic::assignable<__type12>::type __type13;
      typedef __type13 __type16;
      typedef typename polynomial_matrix::type<__type3, __type7, __type16>::__ptype0 __type17;
      typedef container<typename std::remove_reference<__type17>::type> __type18;
      typedef typename __combined<__type13,__type18>::type __type19;
      typedef typename __combined<__type16,__type18>::type __type20;
      typedef typename polynomial_matrix::type<__type3, __type7, __type20>::__ptype1 __type21;
      typedef indexable<__type21> __type22;
      typedef typename __combined<__type19,__type22>::type __type23;
      typedef typename __combined<__type20,__type22>::type __type24;
      typedef typename __combined<__type23,__type24>::type __type25;
      typedef __type25 __type26;
      typedef typename pythonic::returnable<__type26>::type __type27;
      typedef __type27 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& x, argument_type1&& powers) const
    ;
  }  ;
  struct NAME_TO_FUNC
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef linear __type1;
      typedef pythonic::types::dict<__type0,__type1> __type2;
      typedef thin_plate_spline __type3;
      typedef pythonic::types::dict<__type0,__type3> __type4;
      typedef typename __combined<__type2,__type4>::type __type5;
      typedef cubic __type6;
      typedef pythonic::types::dict<__type0,__type6> __type7;
      typedef typename __combined<__type5,__type7>::type __type8;
      typedef quintic __type9;
      typedef pythonic::types::dict<__type0,__type9> __type10;
      typedef typename __combined<__type8,__type10>::type __type11;
      typedef multiquadric __type12;
      typedef pythonic::types::dict<__type0,__type12> __type13;
      typedef typename __combined<__type11,__type13>::type __type14;
      typedef inverse_multiquadric __type15;
      typedef pythonic::types::dict<__type0,__type15> __type16;
      typedef typename __combined<__type14,__type16>::type __type17;
      typedef inverse_quadratic __type18;
      typedef pythonic::types::dict<__type0,__type18> __type19;
      typedef typename __combined<__type17,__type19>::type __type20;
      typedef gaussian __type21;
      typedef pythonic::types::dict<__type0,__type21> __type22;
      typedef typename __combined<__type20,__type22>::type __type23;
      typedef typename pythonic::returnable<__type23>::type __type24;
      typedef __type24 result_type;
    }  ;
    inline
    typename type::result_type operator()() const;
    ;
  }  ;
  struct _kernel_matrix
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>(), std::declval<__type5>())) __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type10;
      typedef decltype(std::declval<__type0>()(std::declval<__type9>(), std::declval<__type10>())) __type11;
      typedef typename pythonic::assignable<__type11>::type __type12;
      typedef pythonic::types::str __type14;
      typedef linear __type15;
      typedef pythonic::types::dict<__type14,__type15> __type16;
      typedef thin_plate_spline __type17;
      typedef pythonic::types::dict<__type14,__type17> __type18;
      typedef typename __combined<__type16,__type18>::type __type19;
      typedef cubic __type20;
      typedef pythonic::types::dict<__type14,__type20> __type21;
      typedef typename __combined<__type19,__type21>::type __type22;
      typedef quintic __type23;
      typedef pythonic::types::dict<__type14,__type23> __type24;
      typedef typename __combined<__type22,__type24>::type __type25;
      typedef multiquadric __type26;
      typedef pythonic::types::dict<__type14,__type26> __type27;
      typedef typename __combined<__type25,__type27>::type __type28;
      typedef inverse_multiquadric __type29;
      typedef pythonic::types::dict<__type14,__type29> __type30;
      typedef typename __combined<__type28,__type30>::type __type31;
      typedef inverse_quadratic __type32;
      typedef pythonic::types::dict<__type14,__type32> __type33;
      typedef typename __combined<__type31,__type33>::type __type34;
      typedef gaussian __type35;
      typedef pythonic::types::dict<__type14,__type35> __type36;
      typedef typename __combined<__type34,__type36>::type __type37;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type38;
      typedef __type38 __type39;
      typedef decltype(std::declval<__type37>()[std::declval<__type39>()]) __type40;
      typedef __type12 __type41;
      typedef typename kernel_matrix::type<__type3, __type40, __type41>::__ptype4 __type42;
      typedef container<typename std::remove_reference<__type42>::type> __type43;
      typedef typename __combined<__type12,__type43>::type __type44;
      typedef typename __combined<__type41,__type43>::type __type45;
      typedef typename kernel_matrix::type<__type3, __type40, __type45>::__ptype5 __type46;
      typedef indexable<__type46> __type47;
      typedef typename __combined<__type44,__type47>::type __type48;
      typedef typename __combined<__type45,__type47>::type __type49;
      typedef typename __combined<__type48,__type49>::type __type50;
      typedef __type50 __type51;
      typedef typename pythonic::returnable<__type51>::type __type52;
      typedef __type52 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& x, argument_type1&& kernel) const
    ;
  }  ;
  struct _evaluate
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type7>::type>::type __type6;
      typedef __type6 __type7;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type7>())) __type8;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>(), std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type11;
      typedef decltype(std::declval<__type0>()(std::declval<__type10>(), std::declval<__type11>())) __type12;
      typedef typename pythonic::assignable<__type12>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type14;
      typedef decltype(std::declval<__type14>()(std::declval<__type5>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef __type16 __type17;
      typedef decltype(std::declval<__type14>()(std::declval<__type9>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef __type19 __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type20>())) __type21;
      typedef indexable<__type21> __type22;
      typedef typename __combined<__type13,__type22>::type __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type25;
      typedef __type25 __type26;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type26>())) __type27;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type27>::type>::type __type28;
      typedef typename pythonic::assignable<__type28>::type __type29;
      typedef __type29 __type30;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type31;
      typedef __type31 __type32;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type32>())) __type33;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type33>::type>::type __type34;
      typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type34>())) __type35;
      typedef decltype(std::declval<__type14>()(std::declval<__type35>())) __type36;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type36>::type::iterator>::value_type>::type __type37;
      typedef __type37 __type38;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type38>(), std::declval<__type20>())) __type40;
      typedef decltype(std::declval<__type7>()[std::declval<__type40>()]) __type41;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type42;
      typedef decltype(std::declval<__type1>()(std::declval<__type35>())) __type45;
      typedef decltype(std::declval<__type42>()(std::declval<__type45>(), std::declval<__type11>())) __type46;
      typedef typename pythonic::assignable<__type46>::type __type47;
      typedef __type47 __type48;
      typedef pythonic::types::contiguous_slice __type49;
      typedef decltype(std::declval<__type48>()[std::declval<__type49>()]) __type50;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type52;
      typedef __type52 __type53;
      typedef decltype(pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type53>())) __type54;
      typedef typename pythonic::assignable<__type54>::type __type55;
      typedef __type55 __type56;
      typedef decltype(std::declval<__type56>()[std::declval<__type17>()]) __type58;
      typedef decltype(pythonic::operator_::mul(std::declval<__type26>(), std::declval<__type53>())) __type61;
      typedef typename pythonic::assignable<__type61>::type __type62;
      typedef __type62 __type63;
      typedef pythonic::types::str __type64;
      typedef linear __type65;
      typedef pythonic::types::dict<__type64,__type65> __type66;
      typedef thin_plate_spline __type67;
      typedef pythonic::types::dict<__type64,__type67> __type68;
      typedef typename __combined<__type66,__type68>::type __type69;
      typedef cubic __type70;
      typedef pythonic::types::dict<__type64,__type70> __type71;
      typedef typename __combined<__type69,__type71>::type __type72;
      typedef quintic __type73;
      typedef pythonic::types::dict<__type64,__type73> __type74;
      typedef typename __combined<__type72,__type74>::type __type75;
      typedef multiquadric __type76;
      typedef pythonic::types::dict<__type64,__type76> __type77;
      typedef typename __combined<__type75,__type77>::type __type78;
      typedef inverse_multiquadric __type79;
      typedef pythonic::types::dict<__type64,__type79> __type80;
      typedef typename __combined<__type78,__type80>::type __type81;
      typedef inverse_quadratic __type82;
      typedef pythonic::types::dict<__type64,__type82> __type83;
      typedef typename __combined<__type81,__type83>::type __type84;
      typedef gaussian __type85;
      typedef pythonic::types::dict<__type64,__type85> __type86;
      typedef typename __combined<__type84,__type86>::type __type87;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type88;
      typedef __type88 __type89;
      typedef decltype(std::declval<__type87>()[std::declval<__type89>()]) __type90;
      typedef typename pythonic::assignable<__type90>::type __type91;
      typedef __type91 __type92;
      typedef typename kernel_vector::type<__type58, __type63, __type92, __type50>::__ptype16 __type93;
      typedef container<typename std::remove_reference<__type93>::type> __type94;
      typedef typename __combined<__type50,__type94>::type __type95;
      typedef typename kernel_vector::type<__type58, __type63, __type92, __type95>::__ptype17 __type96;
      typedef indexable<__type96> __type97;
      typedef typename __combined<__type95,__type97>::type __type98;
      typedef typename __combined<__type94,__type97>::type __type99;
      typedef typename __combined<__type47,__type98,__type99>::type __type100;
      typedef __type100 __type101;
      typedef decltype(std::declval<__type101>()[std::declval<__type49>()]) __type102;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type104;
      typedef __type104 __type105;
      typedef decltype(pythonic::operator_::sub(std::declval<__type3>(), std::declval<__type105>())) __type106;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type6>::type>::type __type107;
      typedef __type107 __type108;
      typedef decltype(pythonic::operator_::div(std::declval<__type106>(), std::declval<__type108>())) __type109;
      typedef typename pythonic::assignable<__type109>::type __type110;
      typedef __type110 __type111;
      typedef decltype(std::declval<__type111>()[std::declval<__type17>()]) __type113;
      typedef typename polynomial_vector::type<__type113, __type32, __type102>::__ptype12 __type115;
      typedef container<typename std::remove_reference<__type115>::type> __type116;
      typedef typename __combined<__type102,__type116>::type __type117;
      typedef typename polynomial_vector::type<__type113, __type32, __type117>::__ptype13 __type118;
      typedef indexable<__type118> __type119;
      typedef typename __combined<__type117,__type119>::type __type120;
      typedef typename __combined<__type116,__type119>::type __type121;
      typedef typename __combined<__type47,__type98,__type99,__type120,__type121>::type __type122;
      typedef __type122 __type123;
      typedef decltype(std::declval<__type123>()[std::declval<__type38>()]) __type125;
      typedef decltype(pythonic::operator_::mul(std::declval<__type41>(), std::declval<__type125>())) __type126;
      typedef container<typename std::remove_reference<__type126>::type> __type127;
      typedef typename __combined<__type23,__type22,__type127>::type __type128;
      typedef __type128 __type129;
      typedef typename pythonic::returnable<__type129>::type __type130;
      typedef __type130 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6, argument_type7>::result_type operator()(argument_type0&& x, argument_type1&& y, argument_type2&& kernel, argument_type3&& epsilon, argument_type4&& powers, argument_type5&& shift, argument_type6&& scale, argument_type7&& coeffs) const
    ;
  }  ;
  struct _build_system
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
      typedef __type2 __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef typename pythonic::assignable<__type5>::type __type6;
      typedef __type6 __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type8;
      typedef __type8 __type9;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type9>())) __type10;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type __type11;
      typedef typename pythonic::assignable<__type11>::type __type12;
      typedef __type12 __type13;
      typedef decltype(pythonic::operator_::add(std::declval<__type7>(), std::declval<__type13>())) __type14;
      typedef decltype(std::declval<__type1>()(std::declval<__type14>(), std::declval<__type14>())) __type18;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type19;
      typedef decltype(std::declval<__type0>()(std::declval<__type18>(), std::declval<__type19>())) __type20;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<__type21>::type __type22;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type23;
      typedef decltype(std::declval<__type23>()(std::declval<__type7>())) __type25;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type __type26;
      typedef __type26 __type27;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type27>(), std::declval<__type27>())) __type29;
      typedef indexable<__type29> __type30;
      typedef typename __combined<__type22,__type30>::type __type31;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type32;
      typedef __type32 __type33;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type34;
      typedef __type34 __type35;
      typedef decltype(pythonic::operator_::mul(std::declval<__type33>(), std::declval<__type35>())) __type36;
      typedef pythonic::types::str __type37;
      typedef linear __type38;
      typedef pythonic::types::dict<__type37,__type38> __type39;
      typedef thin_plate_spline __type40;
      typedef pythonic::types::dict<__type37,__type40> __type41;
      typedef typename __combined<__type39,__type41>::type __type42;
      typedef cubic __type43;
      typedef pythonic::types::dict<__type37,__type43> __type44;
      typedef typename __combined<__type42,__type44>::type __type45;
      typedef quintic __type46;
      typedef pythonic::types::dict<__type37,__type46> __type47;
      typedef typename __combined<__type45,__type47>::type __type48;
      typedef multiquadric __type49;
      typedef pythonic::types::dict<__type37,__type49> __type50;
      typedef typename __combined<__type48,__type50>::type __type51;
      typedef inverse_multiquadric __type52;
      typedef pythonic::types::dict<__type37,__type52> __type53;
      typedef typename __combined<__type51,__type53>::type __type54;
      typedef inverse_quadratic __type55;
      typedef pythonic::types::dict<__type37,__type55> __type56;
      typedef typename __combined<__type54,__type56>::type __type57;
      typedef gaussian __type58;
      typedef pythonic::types::dict<__type37,__type58> __type59;
      typedef typename __combined<__type57,__type59>::type __type60;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type61;
      typedef __type61 __type62;
      typedef decltype(std::declval<__type60>()[std::declval<__type62>()]) __type63;
      typedef __type22 __type64;
      typedef pythonic::types::contiguous_slice __type65;
      typedef decltype(std::declval<__type64>()(std::declval<__type65>(), std::declval<__type65>())) __type66;
      typedef typename kernel_matrix::type<__type36, __type63, __type66>::__ptype4 __type67;
      typedef container<typename std::remove_reference<__type67>::type> __type68;
      typedef container<typename std::remove_reference<__type68>::type> __type69;
      typedef typename kernel_matrix::type<__type36, __type63, __type66>::__ptype5 __type70;
      typedef indexable<__type70> __type71;
      typedef container<typename std::remove_reference<__type71>::type> __type72;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::max{})>::type>::type __type74;
      typedef long __type76;
      typedef decltype(std::declval<__type74>()(std::declval<__type33>(), std::declval<__type76>())) __type77;
      typedef typename pythonic::assignable<__type77>::type __type78;
      typedef __type78 __type79;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::min{})>::type>::type __type80;
      typedef decltype(std::declval<__type80>()(std::declval<__type33>(), std::declval<__type76>())) __type82;
      typedef typename pythonic::assignable<__type82>::type __type83;
      typedef __type83 __type84;
      typedef decltype(pythonic::operator_::add(std::declval<__type79>(), std::declval<__type84>())) __type85;
      typedef decltype(pythonic::operator_::div(std::declval<__type85>(), std::declval<__type76>())) __type86;
      typedef typename pythonic::assignable<__type86>::type __type87;
      typedef __type87 __type88;
      typedef decltype(pythonic::operator_::sub(std::declval<__type33>(), std::declval<__type88>())) __type89;
      typedef decltype(pythonic::operator_::sub(std::declval<__type79>(), std::declval<__type84>())) __type92;
      typedef decltype(pythonic::operator_::div(std::declval<__type92>(), std::declval<__type76>())) __type93;
      typedef typename pythonic::assignable<__type93>::type __type94;
      typedef double __type95;
      typedef container<typename std::remove_reference<__type95>::type> __type96;
      typedef typename __combined<__type94,__type96>::type __type97;
      typedef __type97 __type98;
      typedef decltype(pythonic::operator_::eq(std::declval<__type98>(), std::declval<__type95>())) __type99;
      typedef indexable<__type99> __type100;
      typedef typename __combined<__type94,__type100>::type __type101;
      typedef typename __combined<__type101,__type96,__type100,__type96>::type __type102;
      typedef __type102 __type103;
      typedef decltype(pythonic::operator_::div(std::declval<__type89>(), std::declval<__type103>())) __type104;
      typedef typename __combined<__type22,__type69,__type72>::type __type106;
      typedef __type106 __type107;
      typedef decltype(std::declval<__type107>()(std::declval<__type65>(), std::declval<__type65>())) __type108;
      typedef typename polynomial_matrix::type<__type104, __type9, __type108>::__ptype0 __type109;
      typedef container<typename std::remove_reference<__type109>::type> __type110;
      typedef container<typename std::remove_reference<__type110>::type> __type111;
      typedef typename polynomial_matrix::type<__type104, __type9, __type108>::__ptype1 __type112;
      typedef indexable<__type112> __type113;
      typedef container<typename std::remove_reference<__type113>::type> __type114;
      typedef typename __combined<__type22,__type69,__type72,__type111,__type114>::type __type115;
      typedef __type115 __type116;
      typedef decltype(std::declval<__type116>()(std::declval<__type65>(), std::declval<__type65>())) __type117;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type117>())) __type118;
      typedef container<typename std::remove_reference<__type118>::type> __type119;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type120;
      typedef __type120 __type121;
      typedef decltype(std::declval<__type121>()[std::declval<__type27>()]) __type123;
      typedef container<typename std::remove_reference<__type123>::type> __type124;
      typedef typename __combined<__type31,__type69,__type72,__type111,__type114,__type119,__type96,__type30,__type124>::type __type125;
      typedef __type125 __type126;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type129;
      typedef decltype(std::declval<__type1>()(std::declval<__type129>(), std::declval<__type14>())) __type133;
      typedef decltype(std::declval<__type0>()(std::declval<__type133>(), std::declval<__type19>())) __type134;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type134>())) __type135;
      typedef typename pythonic::assignable<__type135>::type __type136;
      typedef typename __combined<__type136,__type3,__type95>::type __type138;
      typedef __type138 __type139;
      typedef typename __combined<__type101,__type96,__type100>::type __type141;
      typedef __type141 __type142;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type126>(), std::declval<__type139>(), std::declval<__type88>(), std::declval<__type142>())) __type143;
      typedef typename pythonic::returnable<__type143>::type __type144;
      typedef __type144 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& y, argument_type1&& d, argument_type2&& smoothing, argument_type3&& kernel, argument_type4&& epsilon, argument_type5&& powers) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename polynomial_matrix::type<argument_type0, argument_type1, argument_type2>::result_type polynomial_matrix::operator()(argument_type0&& x, argument_type1&& powers, argument_type2&& out) const
  {
    {
      long  __target139832513282880 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x));
      for (long  i=0L; i < __target139832513282880; i += 1L)
      {
        {
          long  __target139832513344800 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers));
          for (long  j=0L; j < __target139832513344800; j += 1L)
          {
            out.fast(pythonic::types::make_tuple(i, j)) = pythonic::numpy::functor::prod{}(pythonic::builtins::pow(x.fast(i), powers.fast(j)));
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename kernel_matrix::type<argument_type0, argument_type1, argument_type2>::result_type kernel_matrix::operator()(argument_type0&& x, argument_type1&& kernel_func, argument_type2&& out) const
  {
    {
      long  __target139832513854048 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x));
      for (long  i=0L; i < __target139832513854048; i += 1L)
      {
        {
          long  __target139832513283024 = pythonic::operator_::add(i, 1L);
          for (long  j=0L; j < __target139832513283024; j += 1L)
          {
            out.fast(pythonic::types::make_tuple(i, j)) = kernel_func(pythonic::numpy::linalg::functor::norm{}(pythonic::operator_::sub(x.fast(i), x.fast(j))));
            out.fast(pythonic::types::make_tuple(j, i)) = out.fast(pythonic::types::make_tuple(i, j));
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename polynomial_vector::type<argument_type0, argument_type1, argument_type2>::result_type polynomial_vector::operator()(argument_type0&& x, argument_type1&& powers, argument_type2&& out) const
  {
    {
      long  __target139832513851840 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers));
      for (long  i=0L; i < __target139832513851840; i += 1L)
      {
        out.fast(i) = pythonic::numpy::functor::prod{}(pythonic::builtins::pow(x, powers.fast(i)));
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename kernel_vector::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type kernel_vector::operator()(argument_type0&& x, argument_type1&& y, argument_type2&& kernel_func, argument_type3&& out) const
  {
    {
      long  __target139832513899296 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, y));
      for (long  i=0L; i < __target139832513899296; i += 1L)
      {
        out.fast(i) = kernel_func(pythonic::numpy::linalg::functor::norm{}(pythonic::operator_::sub(x, y.fast(i))));
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 >
  inline
  typename gaussian::type<argument_type0>::result_type gaussian::operator()(argument_type0&& r) const
  {
    return pythonic::numpy::functor::exp{}(pythonic::operator_::neg(pythonic::numpy::functor::square{}(r)));
  }
  template <typename argument_type0 >
  inline
  typename inverse_quadratic::type<argument_type0>::result_type inverse_quadratic::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::div(1L, pythonic::operator_::add(pythonic::numpy::functor::square{}(r), 1L));
  }
  template <typename argument_type0 >
  inline
  typename inverse_multiquadric::type<argument_type0>::result_type inverse_multiquadric::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::div(1L, pythonic::numpy::functor::sqrt{}(pythonic::operator_::add(pythonic::numpy::functor::square{}(r), 1L)));
  }
  template <typename argument_type0 >
  inline
  typename multiquadric::type<argument_type0>::result_type multiquadric::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::neg(pythonic::numpy::functor::sqrt{}(pythonic::operator_::add(pythonic::numpy::functor::square{}(r), 1L)));
  }
  template <typename argument_type0 >
  inline
  typename quintic::type<argument_type0>::result_type quintic::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::neg(pythonic::operator_::mul(pythonic::numpy::functor::square{}(pythonic::numpy::functor::square{}(r)), r));
  }
  template <typename argument_type0 >
  inline
  typename cubic::type<argument_type0>::result_type cubic::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::mul(pythonic::numpy::functor::square{}(r), r);
  }
  template <typename argument_type0 >
  inline
  typename thin_plate_spline::type<argument_type0>::result_type thin_plate_spline::operator()(argument_type0&& r) const
  {
    if (pythonic::operator_::eq(r, 0L))
    {
      return 0.0;
    }
    else
    {
      return pythonic::operator_::mul(pythonic::numpy::functor::square{}(r), pythonic::numpy::functor::log{}(r));
    }
  }
  template <typename argument_type0 >
  inline
  typename linear::type<argument_type0>::result_type linear::operator()(argument_type0&& r) const
  {
    return pythonic::operator_::neg(r);
  }
  template <typename argument_type0 , typename argument_type1 >
  inline
  typename _polynomial_matrix::type<argument_type0, argument_type1>::result_type _polynomial_matrix::operator()(argument_type0&& x, argument_type1&& powers) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef __type2 __type3;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
    typedef __type6 __type7;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
    typedef decltype(std::declval<__type1>()(std::declval<__type5>(), std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type11;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>(), std::declval<__type11>())) __type12;
    typedef typename pythonic::assignable<__type12>::type __type13;
    typedef __type13 __type16;
    typedef typename polynomial_matrix::type<__type3, __type7, __type16>::__ptype0 __type17;
    typedef container<typename std::remove_reference<__type17>::type> __type18;
    typedef typename __combined<__type13,__type18>::type __type19;
    typedef typename __combined<__type16,__type18>::type __type20;
    typedef typename polynomial_matrix::type<__type3, __type7, __type20>::__ptype1 __type21;
    typedef indexable<__type21> __type22;
    typedef typename __combined<__type19,__type22>::type __type23;
    typedef typename __combined<__type20,__type22>::type __type24;
    typedef typename __combined<__type23,__type24>::type __type25;
    typedef typename pythonic::assignable<__type25>::type __type26;
    __type26 out = pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers))), pythonic::builtins::functor::float_{});
    polynomial_matrix()(x, powers, out);
    return out;
  }
  inline
  typename NAME_TO_FUNC::type::result_type NAME_TO_FUNC::operator()() const
  {
    {
      static typename NAME_TO_FUNC::type::result_type tmp_global = typename pythonic::assignable<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<pythonic::types::dict<pythonic::types::str,linear>,pythonic::types::dict<pythonic::types::str,thin_plate_spline>>::type,pythonic::types::dict<pythonic::types::str,cubic>>::type,pythonic::types::dict<pythonic::types::str,quintic>>::type,pythonic::types::dict<pythonic::types::str,multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_quadratic>>::type,pythonic::types::dict<pythonic::types::str,gaussian>>::type>::type{{{ pythonic::types::str("linear"), linear() }, { pythonic::types::str("thin_plate_spline"), thin_plate_spline() }, { pythonic::types::str("cubic"), cubic() }, { pythonic::types::str("quintic"), quintic() }, { pythonic::types::str("multiquadric"), multiquadric() }, { pythonic::types::str("inverse_multiquadric"), inverse_multiquadric() }, { pythonic::types::str("inverse_quadratic"), inverse_quadratic() }, { pythonic::types::str("gaussian"), gaussian() }}};
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  inline
  typename _kernel_matrix::type<argument_type0, argument_type1>::result_type _kernel_matrix::operator()(argument_type0&& x, argument_type1&& kernel) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef __type2 __type3;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
    typedef decltype(std::declval<__type1>()(std::declval<__type5>(), std::declval<__type5>())) __type9;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type9>(), std::declval<__type10>())) __type11;
    typedef typename pythonic::assignable<__type11>::type __type12;
    typedef pythonic::types::str __type14;
    typedef linear __type15;
    typedef pythonic::types::dict<__type14,__type15> __type16;
    typedef thin_plate_spline __type17;
    typedef pythonic::types::dict<__type14,__type17> __type18;
    typedef typename __combined<__type16,__type18>::type __type19;
    typedef cubic __type20;
    typedef pythonic::types::dict<__type14,__type20> __type21;
    typedef typename __combined<__type19,__type21>::type __type22;
    typedef quintic __type23;
    typedef pythonic::types::dict<__type14,__type23> __type24;
    typedef typename __combined<__type22,__type24>::type __type25;
    typedef multiquadric __type26;
    typedef pythonic::types::dict<__type14,__type26> __type27;
    typedef typename __combined<__type25,__type27>::type __type28;
    typedef inverse_multiquadric __type29;
    typedef pythonic::types::dict<__type14,__type29> __type30;
    typedef typename __combined<__type28,__type30>::type __type31;
    typedef inverse_quadratic __type32;
    typedef pythonic::types::dict<__type14,__type32> __type33;
    typedef typename __combined<__type31,__type33>::type __type34;
    typedef gaussian __type35;
    typedef pythonic::types::dict<__type14,__type35> __type36;
    typedef typename __combined<__type34,__type36>::type __type37;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type38;
    typedef __type38 __type39;
    typedef decltype(std::declval<__type37>()[std::declval<__type39>()]) __type40;
    typedef __type12 __type41;
    typedef typename kernel_matrix::type<__type3, __type40, __type41>::__ptype4 __type42;
    typedef container<typename std::remove_reference<__type42>::type> __type43;
    typedef typename __combined<__type12,__type43>::type __type44;
    typedef typename __combined<__type41,__type43>::type __type45;
    typedef typename kernel_matrix::type<__type3, __type40, __type45>::__ptype5 __type46;
    typedef indexable<__type46> __type47;
    typedef typename __combined<__type44,__type47>::type __type48;
    typedef typename __combined<__type45,__type47>::type __type49;
    typedef typename __combined<__type48,__type49>::type __type50;
    typedef typename pythonic::assignable<__type50>::type __type51;
    __type51 out = pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x))), pythonic::builtins::functor::float_{});
    kernel_matrix()(x, typename pythonic::assignable<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<pythonic::types::dict<pythonic::types::str,linear>,pythonic::types::dict<pythonic::types::str,thin_plate_spline>>::type,pythonic::types::dict<pythonic::types::str,cubic>>::type,pythonic::types::dict<pythonic::types::str,quintic>>::type,pythonic::types::dict<pythonic::types::str,multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_quadratic>>::type,pythonic::types::dict<pythonic::types::str,gaussian>>::type>::type{{{ pythonic::types::str("linear"), linear() }, { pythonic::types::str("thin_plate_spline"), thin_plate_spline() }, { pythonic::types::str("cubic"), cubic() }, { pythonic::types::str("quintic"), quintic() }, { pythonic::types::str("multiquadric"), multiquadric() }, { pythonic::types::str("inverse_multiquadric"), inverse_multiquadric() }, { pythonic::types::str("inverse_quadratic"), inverse_quadratic() }, { pythonic::types::str("gaussian"), gaussian() }}}[kernel], out);
    return out;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 >
  inline
  typename _evaluate::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6, argument_type7>::result_type _evaluate::operator()(argument_type0&& x, argument_type1&& y, argument_type2&& kernel, argument_type3&& epsilon, argument_type4&& powers, argument_type5&& shift, argument_type6&& scale, argument_type7&& coeffs) const
  {
    typedef pythonic::types::str __type0;
    typedef linear __type1;
    typedef pythonic::types::dict<__type0,__type1> __type2;
    typedef thin_plate_spline __type3;
    typedef pythonic::types::dict<__type0,__type3> __type4;
    typedef typename __combined<__type2,__type4>::type __type5;
    typedef cubic __type6;
    typedef pythonic::types::dict<__type0,__type6> __type7;
    typedef typename __combined<__type5,__type7>::type __type8;
    typedef quintic __type9;
    typedef pythonic::types::dict<__type0,__type9> __type10;
    typedef typename __combined<__type8,__type10>::type __type11;
    typedef multiquadric __type12;
    typedef pythonic::types::dict<__type0,__type12> __type13;
    typedef typename __combined<__type11,__type13>::type __type14;
    typedef inverse_multiquadric __type15;
    typedef pythonic::types::dict<__type0,__type15> __type16;
    typedef typename __combined<__type14,__type16>::type __type17;
    typedef inverse_quadratic __type18;
    typedef pythonic::types::dict<__type0,__type18> __type19;
    typedef typename __combined<__type17,__type19>::type __type20;
    typedef gaussian __type21;
    typedef pythonic::types::dict<__type0,__type21> __type22;
    typedef typename __combined<__type20,__type22>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type24;
    typedef __type24 __type25;
    typedef decltype(std::declval<__type23>()[std::declval<__type25>()]) __type26;
    typedef typename pythonic::assignable<__type26>::type __type27;
    typedef typename pythonic::assignable<__type27>::type __type28;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type29;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type30;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type31;
    typedef __type31 __type32;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type32>())) __type33;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type33>::type>::type __type34;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type7>::type>::type __type35;
    typedef __type35 __type36;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type36>())) __type37;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type37>::type>::type __type38;
    typedef decltype(std::declval<__type30>()(std::declval<__type34>(), std::declval<__type38>())) __type39;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type40;
    typedef decltype(std::declval<__type29>()(std::declval<__type39>(), std::declval<__type40>())) __type41;
    typedef typename pythonic::assignable<__type41>::type __type42;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type43;
    typedef decltype(std::declval<__type43>()(std::declval<__type34>())) __type44;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type44>::type::iterator>::value_type>::type __type45;
    typedef __type45 __type46;
    typedef decltype(std::declval<__type43>()(std::declval<__type38>())) __type47;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type47>::type::iterator>::value_type>::type __type48;
    typedef __type48 __type49;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type46>(), std::declval<__type49>())) __type50;
    typedef indexable<__type50> __type51;
    typedef typename __combined<__type42,__type51>::type __type52;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type54;
    typedef __type54 __type55;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type55>())) __type56;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type56>::type>::type __type57;
    typedef typename pythonic::assignable<__type57>::type __type58;
    typedef __type58 __type59;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type60;
    typedef __type60 __type61;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type61>())) __type62;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type62>::type>::type __type63;
    typedef decltype(pythonic::operator_::add(std::declval<__type59>(), std::declval<__type63>())) __type64;
    typedef decltype(std::declval<__type43>()(std::declval<__type64>())) __type65;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type65>::type::iterator>::value_type>::type __type66;
    typedef __type66 __type67;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type67>(), std::declval<__type49>())) __type69;
    typedef decltype(std::declval<__type36>()[std::declval<__type69>()]) __type70;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type71;
    typedef decltype(std::declval<__type30>()(std::declval<__type64>())) __type74;
    typedef decltype(std::declval<__type71>()(std::declval<__type74>(), std::declval<__type40>())) __type75;
    typedef typename pythonic::assignable<__type75>::type __type76;
    typedef __type76 __type77;
    typedef pythonic::types::contiguous_slice __type78;
    typedef decltype(std::declval<__type77>()[std::declval<__type78>()]) __type79;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type81;
    typedef __type81 __type82;
    typedef decltype(pythonic::operator_::mul(std::declval<__type32>(), std::declval<__type82>())) __type83;
    typedef typename pythonic::assignable<__type83>::type __type84;
    typedef __type84 __type85;
    typedef decltype(std::declval<__type85>()[std::declval<__type46>()]) __type87;
    typedef decltype(pythonic::operator_::mul(std::declval<__type55>(), std::declval<__type82>())) __type90;
    typedef typename pythonic::assignable<__type90>::type __type91;
    typedef __type91 __type92;
    typedef __type27 __type93;
    typedef typename kernel_vector::type<__type87, __type92, __type93, __type79>::__ptype16 __type94;
    typedef container<typename std::remove_reference<__type94>::type> __type95;
    typedef typename __combined<__type79,__type95>::type __type96;
    typedef typename kernel_vector::type<__type87, __type92, __type93, __type96>::__ptype17 __type97;
    typedef indexable<__type97> __type98;
    typedef typename __combined<__type96,__type98>::type __type99;
    typedef typename __combined<__type95,__type98>::type __type100;
    typedef typename __combined<__type76,__type99,__type100>::type __type101;
    typedef __type101 __type102;
    typedef decltype(std::declval<__type102>()[std::declval<__type78>()]) __type103;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type105;
    typedef __type105 __type106;
    typedef decltype(pythonic::operator_::sub(std::declval<__type32>(), std::declval<__type106>())) __type107;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type6>::type>::type __type108;
    typedef __type108 __type109;
    typedef decltype(pythonic::operator_::div(std::declval<__type107>(), std::declval<__type109>())) __type110;
    typedef typename pythonic::assignable<__type110>::type __type111;
    typedef __type111 __type112;
    typedef decltype(std::declval<__type112>()[std::declval<__type46>()]) __type114;
    typedef typename polynomial_vector::type<__type114, __type61, __type103>::__ptype12 __type116;
    typedef container<typename std::remove_reference<__type116>::type> __type117;
    typedef typename __combined<__type103,__type117>::type __type118;
    typedef typename polynomial_vector::type<__type114, __type61, __type118>::__ptype13 __type119;
    typedef indexable<__type119> __type120;
    typedef typename __combined<__type118,__type120>::type __type121;
    typedef typename __combined<__type117,__type120>::type __type122;
    typedef typename __combined<__type76,__type99,__type100,__type121,__type122>::type __type123;
    typedef __type123 __type124;
    typedef decltype(std::declval<__type124>()[std::declval<__type67>()]) __type126;
    typedef decltype(pythonic::operator_::mul(std::declval<__type70>(), std::declval<__type126>())) __type127;
    typedef container<typename std::remove_reference<__type127>::type> __type128;
    typedef typename __combined<__type52,__type51,__type128>::type __type129;
    typedef typename pythonic::assignable<__type129>::type __type130;
    typedef typename pythonic::assignable<__type123>::type __type131;
    typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, y)))>::type p = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, y));
    __type28 kernel_func = typename pythonic::assignable<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<pythonic::types::dict<pythonic::types::str,linear>,pythonic::types::dict<pythonic::types::str,thin_plate_spline>>::type,pythonic::types::dict<pythonic::types::str,cubic>>::type,pythonic::types::dict<pythonic::types::str,quintic>>::type,pythonic::types::dict<pythonic::types::str,multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_quadratic>>::type,pythonic::types::dict<pythonic::types::str,gaussian>>::type>::type{{{ pythonic::types::str("linear"), linear() }, { pythonic::types::str("thin_plate_spline"), thin_plate_spline() }, { pythonic::types::str("cubic"), cubic() }, { pythonic::types::str("quintic"), quintic() }, { pythonic::types::str("multiquadric"), multiquadric() }, { pythonic::types::str("inverse_multiquadric"), inverse_multiquadric() }, { pythonic::types::str("inverse_quadratic"), inverse_quadratic() }, { pythonic::types::str("gaussian"), gaussian() }}}[kernel];
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::mul(y, epsilon))>::type yeps = pythonic::operator_::mul(y, epsilon);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::mul(x, epsilon))>::type xeps = pythonic::operator_::mul(x, epsilon);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::operator_::sub(x, shift), scale))>::type xhat = pythonic::operator_::div(pythonic::operator_::sub(x, shift), scale);
    __type130 out = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, coeffs))), pythonic::builtins::functor::float_{});
    __type131 vec = pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::operator_::add(p, std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers)))), pythonic::builtins::functor::float_{});
    {
      long  __target139832513495776 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x));
      for (long  i=0L; i < __target139832513495776; i += 1L)
      {
        kernel_vector()(xeps[i], yeps, kernel_func, vec[pythonic::types::contiguous_slice(pythonic::builtins::None,p)]);
        polynomial_vector()(xhat[i], powers, vec[pythonic::types::contiguous_slice(p,pythonic::builtins::None)]);
        {
          long  __target139832513498704 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, coeffs));
          for (long  j=0L; j < __target139832513498704; j += 1L)
          {
            {
              long  __target139832513513360 = pythonic::operator_::add(p, std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers)));
              for (long  k=0L; k < __target139832513513360; k += 1L)
              {
                out.fast(pythonic::types::make_tuple(i, j)) += pythonic::operator_::mul(coeffs.fast(pythonic::types::make_tuple(k, j)), vec.fast(k));
              }
            }
          }
        }
      }
    }
    return out;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  inline
  typename _build_system::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type _build_system::operator()(argument_type0&& y, argument_type1&& d, argument_type2&& smoothing, argument_type3&& kernel, argument_type4&& epsilon, argument_type5&& powers) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::max{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef __type1 __type2;
    typedef long __type3;
    typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
    typedef typename pythonic::assignable<__type4>::type __type5;
    typedef __type5 __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::min{})>::type>::type __type7;
    typedef decltype(std::declval<__type7>()(std::declval<__type2>(), std::declval<__type3>())) __type9;
    typedef typename pythonic::assignable<__type9>::type __type10;
    typedef __type10 __type11;
    typedef decltype(pythonic::operator_::sub(std::declval<__type6>(), std::declval<__type11>())) __type12;
    typedef decltype(pythonic::operator_::div(std::declval<__type12>(), std::declval<__type3>())) __type13;
    typedef typename pythonic::assignable<__type13>::type __type14;
    typedef double __type15;
    typedef container<typename std::remove_reference<__type15>::type> __type16;
    typedef typename __combined<__type14,__type16>::type __type17;
    typedef __type17 __type18;
    typedef decltype(pythonic::operator_::eq(std::declval<__type18>(), std::declval<__type15>())) __type19;
    typedef indexable<__type19> __type20;
    typedef typename __combined<__type14,__type20>::type __type21;
    typedef typename __combined<__type21,__type16,__type20>::type __type22;
    typedef typename pythonic::assignable<__type22>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type24;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type25;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type26;
    typedef __type26 __type27;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type27>())) __type28;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type28>::type>::type __type29;
    typedef typename pythonic::assignable<__type29>::type __type30;
    typedef __type30 __type31;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type32;
    typedef __type32 __type33;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type33>())) __type34;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type34>::type>::type __type35;
    typedef typename pythonic::assignable<__type35>::type __type36;
    typedef __type36 __type37;
    typedef decltype(pythonic::operator_::add(std::declval<__type31>(), std::declval<__type37>())) __type38;
    typedef decltype(std::declval<__type25>()(std::declval<__type38>(), std::declval<__type38>())) __type42;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::float_{})>::type>::type __type43;
    typedef decltype(std::declval<__type24>()(std::declval<__type42>(), std::declval<__type43>())) __type44;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type44>())) __type45;
    typedef typename pythonic::assignable<__type45>::type __type46;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type47;
    typedef decltype(std::declval<__type47>()(std::declval<__type31>())) __type49;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type49>::type::iterator>::value_type>::type __type50;
    typedef __type50 __type51;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type51>())) __type53;
    typedef indexable<__type53> __type54;
    typedef typename __combined<__type46,__type54>::type __type55;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type57;
    typedef __type57 __type58;
    typedef decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type58>())) __type59;
    typedef pythonic::types::str __type60;
    typedef linear __type61;
    typedef pythonic::types::dict<__type60,__type61> __type62;
    typedef thin_plate_spline __type63;
    typedef pythonic::types::dict<__type60,__type63> __type64;
    typedef typename __combined<__type62,__type64>::type __type65;
    typedef cubic __type66;
    typedef pythonic::types::dict<__type60,__type66> __type67;
    typedef typename __combined<__type65,__type67>::type __type68;
    typedef quintic __type69;
    typedef pythonic::types::dict<__type60,__type69> __type70;
    typedef typename __combined<__type68,__type70>::type __type71;
    typedef multiquadric __type72;
    typedef pythonic::types::dict<__type60,__type72> __type73;
    typedef typename __combined<__type71,__type73>::type __type74;
    typedef inverse_multiquadric __type75;
    typedef pythonic::types::dict<__type60,__type75> __type76;
    typedef typename __combined<__type74,__type76>::type __type77;
    typedef inverse_quadratic __type78;
    typedef pythonic::types::dict<__type60,__type78> __type79;
    typedef typename __combined<__type77,__type79>::type __type80;
    typedef gaussian __type81;
    typedef pythonic::types::dict<__type60,__type81> __type82;
    typedef typename __combined<__type80,__type82>::type __type83;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type84;
    typedef __type84 __type85;
    typedef decltype(std::declval<__type83>()[std::declval<__type85>()]) __type86;
    typedef __type46 __type87;
    typedef pythonic::types::contiguous_slice __type88;
    typedef decltype(std::declval<__type87>()(std::declval<__type88>(), std::declval<__type88>())) __type89;
    typedef typename kernel_matrix::type<__type59, __type86, __type89>::__ptype4 __type90;
    typedef container<typename std::remove_reference<__type90>::type> __type91;
    typedef container<typename std::remove_reference<__type91>::type> __type92;
    typedef typename kernel_matrix::type<__type59, __type86, __type89>::__ptype5 __type93;
    typedef indexable<__type93> __type94;
    typedef container<typename std::remove_reference<__type94>::type> __type95;
    typedef decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type11>())) __type99;
    typedef decltype(pythonic::operator_::div(std::declval<__type99>(), std::declval<__type3>())) __type100;
    typedef typename pythonic::assignable<__type100>::type __type101;
    typedef __type101 __type102;
    typedef decltype(pythonic::operator_::sub(std::declval<__type2>(), std::declval<__type102>())) __type103;
    typedef __type22 __type104;
    typedef decltype(pythonic::operator_::div(std::declval<__type103>(), std::declval<__type104>())) __type105;
    typedef typename __combined<__type46,__type92,__type95>::type __type107;
    typedef __type107 __type108;
    typedef decltype(std::declval<__type108>()(std::declval<__type88>(), std::declval<__type88>())) __type109;
    typedef typename polynomial_matrix::type<__type105, __type33, __type109>::__ptype0 __type110;
    typedef container<typename std::remove_reference<__type110>::type> __type111;
    typedef container<typename std::remove_reference<__type111>::type> __type112;
    typedef typename polynomial_matrix::type<__type105, __type33, __type109>::__ptype1 __type113;
    typedef indexable<__type113> __type114;
    typedef container<typename std::remove_reference<__type114>::type> __type115;
    typedef typename __combined<__type46,__type92,__type95,__type112,__type115>::type __type116;
    typedef __type116 __type117;
    typedef decltype(std::declval<__type117>()(std::declval<__type88>(), std::declval<__type88>())) __type118;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type118>())) __type119;
    typedef container<typename std::remove_reference<__type119>::type> __type120;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type121;
    typedef __type121 __type122;
    typedef decltype(std::declval<__type122>()[std::declval<__type51>()]) __type124;
    typedef container<typename std::remove_reference<__type124>::type> __type125;
    typedef typename __combined<__type55,__type92,__type95,__type112,__type115,__type120,__type16,__type54,__type125>::type __type126;
    typedef typename pythonic::assignable<__type126>::type __type127;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type28>::type>::type __type130;
    typedef decltype(std::declval<__type25>()(std::declval<__type130>(), std::declval<__type38>())) __type134;
    typedef decltype(std::declval<__type24>()(std::declval<__type134>(), std::declval<__type43>())) __type135;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type135>())) __type136;
    typedef typename pythonic::assignable<__type136>::type __type137;
    typedef typename __combined<__type137,__type27,__type15>::type __type139;
    typedef typename pythonic::assignable<__type139>::type __type140;
    typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, d)))>::type p = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, d));
    typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers)))>::type r = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, powers));
    typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::min{}(y, 0L))>::type mins = pythonic::numpy::functor::min{}(y, 0L);
    typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::max{}(y, 0L))>::type maxs = pythonic::numpy::functor::max{}(y, 0L);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::operator_::add(maxs, mins), 2L))>::type shift = pythonic::operator_::div(pythonic::operator_::add(maxs, mins), 2L);
    __type23 scale = pythonic::operator_::div(pythonic::operator_::sub(maxs, mins), 2L);
    scale.fast(pythonic::operator_::eq(scale, 0.0)) = 1.0;
    __type127 lhs = pythonic::builtins::getattr(pythonic::types::attr::T{}, pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::operator_::add(p, r), pythonic::operator_::add(p, r)), pythonic::builtins::functor::float_{}));
    kernel_matrix()(pythonic::operator_::mul(y, epsilon), typename pythonic::assignable<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<typename __combined<pythonic::types::dict<pythonic::types::str,linear>,pythonic::types::dict<pythonic::types::str,thin_plate_spline>>::type,pythonic::types::dict<pythonic::types::str,cubic>>::type,pythonic::types::dict<pythonic::types::str,quintic>>::type,pythonic::types::dict<pythonic::types::str,multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_multiquadric>>::type,pythonic::types::dict<pythonic::types::str,inverse_quadratic>>::type,pythonic::types::dict<pythonic::types::str,gaussian>>::type>::type{{{ pythonic::types::str("linear"), linear() }, { pythonic::types::str("thin_plate_spline"), thin_plate_spline() }, { pythonic::types::str("cubic"), cubic() }, { pythonic::types::str("quintic"), quintic() }, { pythonic::types::str("multiquadric"), multiquadric() }, { pythonic::types::str("inverse_multiquadric"), inverse_multiquadric() }, { pythonic::types::str("inverse_quadratic"), inverse_quadratic() }, { pythonic::types::str("gaussian"), gaussian() }}}[kernel], lhs(pythonic::types::contiguous_slice(pythonic::builtins::None,p),pythonic::types::contiguous_slice(pythonic::builtins::None,p)));
    polynomial_matrix()(pythonic::operator_::div(pythonic::operator_::sub(y, shift), scale), powers, lhs(pythonic::types::contiguous_slice(pythonic::builtins::None,p),pythonic::types::contiguous_slice(p,pythonic::builtins::None)));
    lhs(pythonic::types::contiguous_slice(p,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,p)) = pythonic::builtins::getattr(pythonic::types::attr::T{}, lhs(pythonic::types::contiguous_slice(pythonic::builtins::None,p),pythonic::types::contiguous_slice(p,pythonic::builtins::None)));
    lhs(pythonic::types::contiguous_slice(p,pythonic::builtins::None),pythonic::types::contiguous_slice(p,pythonic::builtins::None)) = 0.0;
    {
      long  __target139832513430816 = p;
      for (long  i=0L; i < __target139832513430816; i += 1L)
      {
        lhs.fast(pythonic::types::make_tuple(i, i)) += smoothing.fast(i);
      }
    }
    __type140 rhs = pythonic::builtins::getattr(pythonic::types::attr::T{}, pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, d)), pythonic::operator_::add(p, r)), pythonic::builtins::functor::float_{}));
    rhs[pythonic::types::contiguous_slice(pythonic::builtins::None,p)] = d;
    rhs[pythonic::types::contiguous_slice(p,pythonic::builtins::None)] = 0.0;
    return pythonic::types::make_tuple(lhs, rhs, shift, scale);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate3(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate4(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate5(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate6(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate7(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate8(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate9(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate10(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate11(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate12(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate13(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _evaluate14(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_evaluate::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _evaluate15(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& shift, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& scale, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& coeffs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_evaluate()(x, y, kernel, epsilon, powers, shift, scale, coeffs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _build_system0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _build_system1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _build_system2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _build_system3(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& y, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _build_system4(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _build_system5(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _build_system6(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_build_system::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::str, double, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _build_system7(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& y, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& d, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& smoothing, pythonic::types::str&& kernel, double&& epsilon, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_build_system()(y, d, smoothing, kernel, epsilon, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_polynomial_matrix::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _polynomial_matrix0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_polynomial_matrix()(x, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_polynomial_matrix::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _polynomial_matrix1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_polynomial_matrix()(x, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_polynomial_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _polynomial_matrix2(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_polynomial_matrix()(x, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_polynomial_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _polynomial_matrix3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& powers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_polynomial_matrix()(x, powers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_kernel_matrix::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::str>::result_type _kernel_matrix0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& x, pythonic::types::str&& kernel) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_kernel_matrix()(x, kernel);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__rbfinterp_pythran::_kernel_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::str>::result_type _kernel_matrix1(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& x, pythonic::types::str&& kernel) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__rbfinterp_pythran::_kernel_matrix()(x, kernel);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap__evaluate0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate3(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate4(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate5(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate6(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate7(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate8(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate9(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate10(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate14(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7]))
        return to_python(_evaluate14(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__evaluate15(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[8+1];
    
    char const* keywords[] = {"x", "y", "kernel", "epsilon", "powers", "shift", "scale", "coeffs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::str>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7]))
        return to_python(_evaluate15(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::str>(args_obj[2]), from_python<double>(args_obj[3]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[6]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[7])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(_build_system0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5]))
        return to_python(_build_system1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(_build_system2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5]))
        return to_python(_build_system3(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(_build_system4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5]))
        return to_python(_build_system5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(_build_system6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__build_system7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"y", "d", "smoothing", "kernel", "epsilon", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::str>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5]))
        return to_python(_build_system7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::str>(args_obj[3]), from_python<double>(args_obj[4]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__polynomial_matrix0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(_polynomial_matrix0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__polynomial_matrix1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(_polynomial_matrix1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__polynomial_matrix2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(_polynomial_matrix2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__polynomial_matrix3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "powers",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(_polynomial_matrix3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__kernel_matrix0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "kernel",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::str>(args_obj[1]))
        return to_python(_kernel_matrix0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::str>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__kernel_matrix1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"x", "kernel",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::str>(args_obj[1]))
        return to_python(_kernel_matrix1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::str>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall__evaluate(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__evaluate0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate7(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate8(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate9(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate11(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate12(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate13(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate14(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__evaluate15(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_evaluate", "\n""    - _evaluate(float[:,:], float[:,:], str, float, int[:,:], float[:], float[:], float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__build_system(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__build_system0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__build_system7(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_build_system", "\n""    - _build_system(float[:,:], float[:,:], float[:], str, float, int[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__polynomial_matrix(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__polynomial_matrix0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__polynomial_matrix1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__polynomial_matrix2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__polynomial_matrix3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_polynomial_matrix", "\n""    - _polynomial_matrix(float[:,:], int[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__kernel_matrix(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__kernel_matrix0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__kernel_matrix1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_kernel_matrix", "\n""    - _kernel_matrix(float[:,:], str)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "_evaluate",
    (PyCFunction)__pythran_wrapall__evaluate,
    METH_VARARGS | METH_KEYWORDS,
    "Evaluate the RBF interpolant at `x`.\n""\n""    Supported prototypes:\n""\n""    - _evaluate(float[:,:], float[:,:], str, float, int[:,:], float[:], float[:], float[:,:])\n""\n""    Parameters\n""    ----------\n""    x : (Q, N) float ndarray\n""        Evaluation point coordinates.\n""    y : (P, N) float ndarray\n""        Data point coordinates.\n""    kernel : str\n""        Name of the RBF.\n""    epsilon : float\n""        Shape parameter.\n""    powers : (R, N) int ndarray\n""        The exponents for each monomial in the polynomial.\n""    shift : (N,) float ndarray\n""        Shifts the polynomial domain for numerical stability.\n""    scale : (N,) float ndarray\n""        Scales the polynomial domain for numerical stability.\n""    coeffs : (P + R, S) float ndarray\n""        Coefficients for each RBF and monomial.\n""\n""    Returns\n""    -------\n""    (Q, S) float ndarray\n""\n"""},{
    "_build_system",
    (PyCFunction)__pythran_wrapall__build_system,
    METH_VARARGS | METH_KEYWORDS,
    "Build the system used to solve for the RBF interpolant coefficients.\n""\n""    Supported prototypes:\n""\n""    - _build_system(float[:,:], float[:,:], float[:], str, float, int[:,:])\n""\n""    Parameters\n""    ----------\n""    y : (P, N) float ndarray\n""        Data point coordinates.\n""    d : (P, S) float ndarray\n""        Data values at `y`.\n""    smoothing : (P,) float ndarray\n""        Smoothing parameter for each data point.\n""    kernel : str\n""        Name of the RBF.\n""    epsilon : float\n""        Shape parameter.\n""    powers : (R, N) int ndarray\n""        The exponents for each monomial in the polynomial.\n""\n""    Returns\n""    -------\n""    lhs : (P + R, P + R) float ndarray\n""        Left-hand side matrix.\n""    rhs : (P + R, S) float ndarray\n""        Right-hand side matrix.\n""    shift : (N,) float ndarray\n""        Domain shift used to create the polynomial matrix.\n""    scale : (N,) float ndarray\n""        Domain scaling used to create the polynomial matrix.\n""\n"""},{
    "_polynomial_matrix",
    (PyCFunction)__pythran_wrapall__polynomial_matrix,
    METH_VARARGS | METH_KEYWORDS,
    "Return monomials, with exponents from `powers`, evaluated at `x`.\n""\n""    Supported prototypes:\n""\n""    - _polynomial_matrix(float[:,:], int[:,:])"},{
    "_kernel_matrix",
    (PyCFunction)__pythran_wrapall__kernel_matrix,
    METH_VARARGS | METH_KEYWORDS,
    "Return RBFs, with centers at `x`, evaluated at `x`.\n""\n""    Supported prototypes:\n""\n""    - _kernel_matrix(float[:,:], str)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_rbfinterp_pythran",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_rbfinterp_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_rbfinterp_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_rbfinterp_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-05-16 07:19:54.263882",
                                      "3c30425550c4548ade4c98d9f66ed93a241515ad72e7efe308ab023945aca246");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif