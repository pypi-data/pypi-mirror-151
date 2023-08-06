#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/int32.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/int32.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/intp.hpp>
#include <pythonic/include/numpy/ndarray/fill.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/ge.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/not_.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/intp.hpp>
#include <pythonic/numpy/ndarray/fill.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/ge.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/not_.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__group_columns
{
  struct group_sparse
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
      typedef decltype(pythonic::operator_::neg(std::declval<__type4>())) __type5;
      typedef typename pythonic::assignable<__type5>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type7;
      typedef decltype(std::declval<__type7>()(std::declval<__type2>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef __type10 __type11;
      typedef indexable<__type11> __type12;
      typedef typename __combined<__type6,__type12>::type __type13;
      typedef long __type14;
      typedef typename pythonic::assignable<__type14>::type __type15;
      typedef __type15 __type16;
      typedef container<typename std::remove_reference<__type16>::type> __type17;
      typedef typename __combined<__type13,__type17,__type12,__type17>::type __type18;
      typedef __type18 __type19;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type19>())) __type20;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
      typedef decltype(std::declval<__type7>()(std::declval<__type21>())) __type22;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type22>::type::iterator>::value_type>::type __type23;
      typedef __type23 __type24;
      typedef indexable<__type24> __type25;
      typedef typename __combined<__type13,__type25>::type __type26;
      typedef typename __combined<__type26,__type17,__type12,__type17,__type25>::type __type29;
      typedef __type29 __type30;
      typedef typename pythonic::returnable<__type30>::type __type31;
      typedef __type31 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& indices, argument_type3&& indptr) const
    ;
  }  ;
  struct group_dense
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
      typedef decltype(pythonic::operator_::neg(std::declval<__type4>())) __type5;
      typedef typename pythonic::assignable<__type5>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type7;
      typedef decltype(std::declval<__type7>()(std::declval<__type2>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef __type10 __type11;
      typedef indexable<__type11> __type12;
      typedef typename __combined<__type6,__type12>::type __type13;
      typedef long __type14;
      typedef typename pythonic::assignable<__type14>::type __type15;
      typedef __type15 __type16;
      typedef container<typename std::remove_reference<__type16>::type> __type17;
      typedef typename __combined<__type13,__type17,__type12,__type17>::type __type18;
      typedef __type18 __type19;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type19>())) __type20;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
      typedef decltype(std::declval<__type7>()(std::declval<__type21>())) __type22;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type22>::type::iterator>::value_type>::type __type23;
      typedef __type23 __type24;
      typedef indexable<__type24> __type25;
      typedef typename __combined<__type13,__type25>::type __type26;
      typedef typename __combined<__type26,__type17,__type12,__type17,__type25>::type __type29;
      typedef __type29 __type30;
      typedef typename pythonic::returnable<__type30>::type __type31;
      typedef __type31 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& A) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename group_sparse::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type group_sparse::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& indices, argument_type3&& indptr) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef __type1 __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type3;
    typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
    typedef decltype(pythonic::operator_::neg(std::declval<__type4>())) __type5;
    typedef typename pythonic::assignable<__type5>::type __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type7;
    typedef decltype(std::declval<__type7>()(std::declval<__type2>())) __type9;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
    typedef __type10 __type11;
    typedef indexable<__type11> __type12;
    typedef typename __combined<__type6,__type12>::type __type13;
    typedef long __type14;
    typedef typename pythonic::assignable<__type14>::type __type15;
    typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type14>())) __type16;
    typedef typename __combined<__type15,__type16>::type __type17;
    typedef typename __combined<__type17,__type14>::type __type18;
    typedef __type18 __type19;
    typedef container<typename std::remove_reference<__type19>::type> __type20;
    typedef typename __combined<__type13,__type20,__type12,__type20>::type __type21;
    typedef __type21 __type22;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type22>())) __type23;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
    typedef decltype(std::declval<__type7>()(std::declval<__type24>())) __type25;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type __type26;
    typedef __type26 __type27;
    typedef indexable<__type27> __type28;
    typedef typename __combined<__type13,__type28>::type __type29;
    typedef typename __combined<__type29,__type20,__type12,__type20,__type28>::type __type32;
    typedef typename pythonic::assignable<__type32>::type __type33;
    typedef typename pythonic::assignable<__type18>::type __type34;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type36;
    typedef __type36 __type37;
    typedef decltype(std::declval<__type35>()(std::declval<__type37>(), std::declval<__type3>())) __type38;
    typedef typename pythonic::assignable<__type38>::type __type39;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type40;
    typedef __type40 __type41;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type42;
    typedef __type42 __type43;
    typedef decltype(std::declval<__type43>()[std::declval<__type11>()]) __type45;
    typedef decltype(pythonic::operator_::add(std::declval<__type11>(), std::declval<__type14>())) __type48;
    typedef decltype(std::declval<__type43>()[std::declval<__type48>()]) __type49;
    typedef decltype(std::declval<__type7>()(std::declval<__type45>(), std::declval<__type49>())) __type50;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type50>::type::iterator>::value_type>::type __type51;
    typedef __type51 __type52;
    typedef decltype(std::declval<__type41>()[std::declval<__type52>()]) __type53;
    typedef indexable<__type53> __type54;
    typedef typename __combined<__type39,__type54>::type __type55;
    typedef decltype(std::declval<__type43>()[std::declval<__type27>()]) __type59;
    typedef decltype(pythonic::operator_::add(std::declval<__type27>(), std::declval<__type14>())) __type62;
    typedef decltype(std::declval<__type43>()[std::declval<__type62>()]) __type63;
    typedef decltype(std::declval<__type7>()(std::declval<__type59>(), std::declval<__type63>())) __type64;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type64>::type::iterator>::value_type>::type __type65;
    typedef __type65 __type66;
    typedef decltype(std::declval<__type41>()[std::declval<__type66>()]) __type67;
    typedef indexable<__type67> __type68;
    typedef typename __combined<__type55,__type68>::type __type69;
    typedef container<typename std::remove_reference<__type14>::type> __type70;
    typedef typename __combined<__type69,__type70,__type54,__type68>::type __type71;
    typedef typename pythonic::assignable<__type71>::type __type72;
    __type33 groups = pythonic::operator_::neg(pythonic::numpy::functor::ones{}(n, pythonic::numpy::functor::intp{}));
    __type34 current_group = 0L;
    __type72 union_ = pythonic::numpy::functor::empty{}(m, pythonic::numpy::functor::intp{});
    {
      long  __target139832508762624 = n;
      for (long  i=0L; i < __target139832508762624; i += 1L)
      {
        if (pythonic::operator_::ge(groups[i], 0L))
        {
          continue;
        }
        groups[i] = current_group;
        typename pythonic::lazy<decltype(true)>::type all_grouped = true;
        pythonic::numpy::ndarray::functor::fill{}(union_, 0L);
        {
          long  __target139832508745184 = indptr[pythonic::operator_::add(i, 1L)];
          for (long  k=indptr[i]; k < __target139832508745184; k += 1L)
          {
            union_[indices[k]] = 1L;
          }
        }
        {
          long  __target139832508745712 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, groups));
          for (long  j=0L; j < __target139832508745712; j += 1L)
          {
            if (pythonic::operator_::lt(groups[j], 0L))
            {
              all_grouped = false;
            }
            else
            {
              continue;
            }
            typename pythonic::lazy<decltype(false)>::type intersect = false;
            {
              long  __target139832508658064 = indptr[pythonic::operator_::add(j, 1L)];
              for (long  k_=indptr[j]; k_ < __target139832508658064; k_ += 1L)
              {
                if (pythonic::operator_::eq(union_[indices[k_]], 1L))
                {
                  intersect = true;
                  break;
                }
              }
            }
            if (pythonic::operator_::not_(intersect))
            {
              {
                long  __target139832508661616 = indptr[pythonic::operator_::add(j, 1L)];
                for (long  k__=indptr[j]; k__ < __target139832508661616; k__ += 1L)
                {
                  union_[indices[k__]] = 1L;
                }
              }
              groups[j] = current_group;
            }
          }
        }
        if (all_grouped)
        {
          break;
        }
        else
        {
          current_group += 1L;
        }
      }
    }
    return groups;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename group_dense::type<argument_type0, argument_type1, argument_type2>::result_type group_dense::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& A) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef __type1 __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type3;
    typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
    typedef decltype(pythonic::operator_::neg(std::declval<__type4>())) __type5;
    typedef typename pythonic::assignable<__type5>::type __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type7;
    typedef decltype(std::declval<__type7>()(std::declval<__type2>())) __type9;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
    typedef __type10 __type11;
    typedef indexable<__type11> __type12;
    typedef typename __combined<__type6,__type12>::type __type13;
    typedef long __type14;
    typedef typename pythonic::assignable<__type14>::type __type15;
    typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type14>())) __type16;
    typedef typename __combined<__type15,__type16>::type __type17;
    typedef typename __combined<__type17,__type14>::type __type18;
    typedef __type18 __type19;
    typedef container<typename std::remove_reference<__type19>::type> __type20;
    typedef typename __combined<__type13,__type20,__type12,__type20>::type __type21;
    typedef __type21 __type22;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type22>())) __type23;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
    typedef decltype(std::declval<__type7>()(std::declval<__type24>())) __type25;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type __type26;
    typedef __type26 __type27;
    typedef indexable<__type27> __type28;
    typedef typename __combined<__type13,__type28>::type __type29;
    typedef typename __combined<__type29,__type20,__type12,__type20,__type28>::type __type32;
    typedef typename pythonic::assignable<__type32>::type __type33;
    typedef typename pythonic::assignable<__type18>::type __type34;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type36;
    typedef __type36 __type37;
    typedef decltype(std::declval<__type35>()(std::declval<__type37>(), std::declval<__type3>())) __type38;
    typedef typename pythonic::assignable<__type38>::type __type39;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type40;
    typedef __type40 __type41;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type41>())) __type42;
    typedef typename pythonic::assignable<__type42>::type __type43;
    typedef __type43 __type44;
    typedef decltype(std::declval<__type44>()[std::declval<__type27>()]) __type46;
    typedef decltype(pythonic::operator_::add(std::declval<__type39>(), std::declval<__type46>())) __type47;
    typedef typename __combined<__type39,__type47>::type __type48;
    typedef decltype(std::declval<__type44>()[std::declval<__type11>()]) __type51;
    typedef typename __combined<__type48,__type51,__type46>::type __type52;
    typedef typename pythonic::assignable<__type52>::type __type53;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, A))>::type B = pythonic::builtins::getattr(pythonic::types::attr::T{}, A);
    __type33 groups = pythonic::operator_::neg(pythonic::numpy::functor::ones{}(n, pythonic::numpy::functor::intp{}));
    __type34 current_group = 0L;
    __type53 union_ = pythonic::numpy::functor::empty{}(m, pythonic::numpy::functor::intp{});
    {
      long  __target139832513453600 = n;
      for (long  i=0L; i < __target139832513453600; i += 1L)
      {
        if (pythonic::operator_::ge(groups[i], 0L))
        {
          continue;
        }
        groups[i] = current_group;
        typename pythonic::lazy<decltype(true)>::type all_grouped = true;
        union_[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = B[i];
        {
          long  __target139832508652224 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, groups));
          for (long  j=0L; j < __target139832508652224; j += 1L)
          {
            if (pythonic::operator_::lt(groups[j], 0L))
            {
              all_grouped = false;
            }
            else
            {
              continue;
            }
            typename pythonic::lazy<decltype(false)>::type intersect = false;
            {
              long  __target139832512276992 = m;
              for (long  k=0L; k < __target139832512276992; k += 1L)
              {
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(union_[k], 0L); }, [&] () { return pythonic::operator_::gt(B[pythonic::types::make_tuple(j, k)], 0L); }))
                {
                  intersect = true;
                  break;
                }
              }
            }
            if (pythonic::operator_::not_(intersect))
            {
              union_ += B[j];
              groups[j] = current_group;
            }
          }
        }
        if (all_grouped)
        {
          break;
        }
        else
        {
          current_group += 1L;
        }
      }
    }
    return groups;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>::result_type group_sparse0(long&& m, long&& n, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indices, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
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
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>::result_type group_sparse1(long&& m, long&& n, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indices, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
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
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::ndarray<long,pythonic::types::pshape<long>>, pythonic::types::ndarray<long,pythonic::types::pshape<long>>>::result_type group_sparse2(long&& m, long&& n, pythonic::types::ndarray<long,pythonic::types::pshape<long>>&& indices, pythonic::types::ndarray<long,pythonic::types::pshape<long>>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
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
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>::result_type group_sparse3(long&& m, long&& n, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>&& indices, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
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
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type group_dense0(long&& m, long&& n, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
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
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type group_dense1(long&& m, long&& n, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
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
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>::result_type group_dense2(long&& m, long&& n, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
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
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>::result_type group_dense3(long&& m, long&& n, pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
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
__pythran_wrap_group_sparse0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3]))
        return to_python(group_sparse0(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3]))
        return to_python(group_sparse1(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(group_sparse2(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(group_sparse3(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[2]))
        return to_python(group_dense0(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[2]))
        return to_python(group_dense1(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>(args_obj[2]))
        return to_python(group_dense2(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>(args_obj[2]))
        return to_python(group_dense3(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_group_sparse(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_group_sparse0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "group_sparse", "\n""    - group_sparse(int, int, int[::], int[::])\n""    - group_sparse(int, int, int32[::], int32[::])\n""    - group_sparse(int, int, int[:], int[:])\n""    - group_sparse(int, int, int32[:], int32[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_group_dense(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_group_dense0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "group_dense", "\n""    - group_dense(int, int, int[:,:])\n""    - group_dense(int, int, int32[:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "group_sparse",
    (PyCFunction)__pythran_wrapall_group_sparse,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - group_sparse(int, int, int[::], int[::])\n""    - group_sparse(int, int, int32[::], int32[::])\n""    - group_sparse(int, int, int[:], int[:])\n""    - group_sparse(int, int, int32[:], int32[:])"},{
    "group_dense",
    (PyCFunction)__pythran_wrapall_group_dense,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - group_dense(int, int, int[:,:])\n""    - group_dense(int, int, int32[:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_group_columns",            /* m_name */
    "\n""Pythran implementation of columns grouping for finite difference Jacobian\n""estimation. Used by ._numdiff.group_columns and based on the Cython version.\n""",         /* m_doc */
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
PYTHRAN_MODULE_INIT(_group_columns)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_group_columns)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_group_columns",
                                         Methods,
                                         "\n""Pythran implementation of columns grouping for finite difference Jacobian\n""estimation. Used by ._numdiff.group_columns and based on the Cython version.\n"""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-05-16 07:19:56.772736",
                                      "bbd9c32ae0cc40f86da54c6bc74a72b8cc51ed42efd9d0a4f45d3648fc5482c3");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif